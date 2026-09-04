# Samvad Setu Mobile App Documentation

## 1. Architecture Overview
The mobile app is built with **React Native** and uses **Expo Router** for file-based routing. It communicates natively with the Express Node.js backend. State management is handled globally by **Zustand**.

### Route Groups
The app leverages Expo Router's Group syntax (parentheses) to strictly separate user flows without exposing them in the URL schema:
- `(auth)`: Contains `login.tsx` and `signup.tsx`.
- `(citizen)`: Citizen dashboard and report submission flows.
- `(hei)` / `(industry)` / `(government)`: Specialized role-based dashboards.

## 2. Authentication Flow

### Global Auth Store (`store/authStore.ts`)
We use Zustand to manage the global authentication state (`user`, `token`, `isLoading`, `error`). 
- **`login(payload)`**: Posts credentials to the backend. On success, it securely saves the JWT and user profile to `SecureStore`.
- **`signup(payload)`**: Posts a new user payload (including complex institutional fields if applicable) to the backend. Saves tokens upon auto-login.
- **`logout()`**: Wipes tokens from `SecureStore` and clears the Zustand state, instantly locking the user out.

### Secure Token Storage
We utilize `expo-secure-store` to safely encrypt the JWT on the native device level. 

### Axios Interceptor (`api/client.ts`)
All backend requests flow through a central Axios instance. An interceptor automatically looks up the token in `SecureStore` and attaches it as a `Bearer` token in the `Authorization` header for every outgoing HTTP request.

## 3. Custom UI Components

### Animated Toast System
We built a custom global Toast messaging system to mirror the premium web UI exactly.
- **`store/toastStore.ts`**: Manages visibility, message string, and type (`success`, `error`, `info`).
- **`components/ui/Toast.tsx`**: Uses React Native's `Animated` API for smooth slide-down and fade-in physics. It dynamically inherits color borders (`#E8A33D`, `#2F9E8F`, `#e74c3c`) and Lucide icons depending on the toast type. It is mounted globally at the root in `app/_layout.tsx`.

## 4. Local Network Testing
For testing on physical Android or iOS devices via Expo Go, the Axios Base URL is bound to the local network IP of the host machine (e.g., `192.168.1.4:5001/api`). Note that `localhost` cannot be used on mobile clients since it resolves to the mobile device itself, not the backend server machine.
