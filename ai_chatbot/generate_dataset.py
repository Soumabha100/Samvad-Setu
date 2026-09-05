import csv
import random
import uuid
import os

categories = [
    "education", "agriculture", "healthcare", "water", "environment", 
    "energy", "urban_development", "accessibility", "public_admin", "rural_livelihoods"
]

locations = ["Ranchi", "Dhanbad", "Jamshedpur", "Bokaro", "Deoghar", "Hazaribagh", "Giridih", "Ramgarh", "Palamu", "Gumla"]

templates = {
    "education": [
        ("The local primary school in {loc} has no roof and leaks during rain.", "English"),
        ("{loc} School mein teacher nahi aate hain pichle ek mahine se.", "Hinglish"),
        ("हमारे {loc} के स्कूल में पीने का पानी नहीं है।", "Hindi"),
        ("Need better library facilities in our government college at {loc}.", "English"),
        ("Exam paper leak ho gaya hai {loc} mein, exams cancel hone chahiye.", "Hinglish"),
        ("बच्चों को {loc} में मिड-डे मील सही से नहीं मिल रहा है।", "Hindi"),
        ("Lack of computer labs in the {loc} high school is affecting students.", "English"),
        ("Teacher vacancy bahut zyada hai {loc} district mein.", "Hinglish"),
        ("विद्यालय का भवन बहुत जर्जर हालत में है {loc} में, कभी भी गिर सकता है।", "Hindi"),
        ("No scholarships have been disbursed in {loc} this year.", "English")
    ],
    "agriculture": [
        ("Crops in {loc} are dying due to lack of irrigation canals.", "English"),
        ("Kisan credit card ka loan maaf nahi hua {loc} mein.", "Hinglish"),
        ("{loc} में खाद और बीज की बहुत कमी है, खेती कैसे करें?", "Hindi"),
        ("Minimum Support Price is not being offered at the {loc} mandi.", "English"),
        ("Fasal bima yojana ka paisa {loc} ke kisano ko nahi mila.", "Hinglish"),
        ("आवारा पशु {loc} में हमारी सारी फसल चर गए हैं।", "Hindi"),
        ("Need soil testing lab in {loc} for better crop yield.", "English"),
        ("Tractor subsidy ka form reject ho gaya {loc} office se.", "Hinglish"),
        ("{loc} में कोल्ड स्टोरेज की सुविधा नहीं চরম है, सब्जियां खराब हो रही हैं।", "Hindi"),
        ("Unseasonal rains have destroyed wheat crops in {loc}.", "English")
    ],
    "healthcare": [
        ("The primary health center in {loc} has no doctors on night duty.", "English"),
        ("{loc} ke hospital mein dawaiyan available nahi hain.", "Hinglish"),
        ("{loc} के अस्पताल में एंबुलेंस की सुविधा नहीं है।", "Hindi"),
        ("Need immediate dengue fogging in {loc} as cases are rising.", "English"),
        ("Covid vaccination center {loc} mein band pada hai.", "Hinglish"),
        ("सरकारी अस्पताल {loc} में डॉक्टर पैसे मांग रहे हैं।", "Hindi"),
        ("No ultrasound machine available in the {loc} district hospital.", "English"),
        ("Ayushman card {loc} ke private hospital mein accept nahi kar rahe.", "Hinglish"),
        ("{loc} में मलेरिया तेजी से फैल रहा है, कोई रोकथाम नहीं है।", "Hindi"),
        ("Maternity ward in {loc} is in unhygienic conditions.", "English")
    ],
    "water": [
        ("No drinking water supply in {loc} for the last 5 days.", "English"),
        ("{loc} mein handpump pichle 2 mahine se kharab hai.", "Hinglish"),
        ("{loc} की पानी की टंकी में गंदगी है और पानी बदबूदार आ रहा है।", "Hindi"),
        ("Pipeline is leaking near the main road in {loc}, wasting water.", "English"),
        ("Water tanker {loc} mein nahi aa raha hai.", "Hinglish"),
        ("हमारे मोहल्ले {loc} में पानी का प्रेशर बहुत कम है।", "Hindi"),
        ("The local pond in {loc} is completely dried up.", "English"),
        ("{loc} mein naya borewell khudwane ki jarurat hai.", "Hinglish"),
        ("{loc} में जल जीवन मिशन का काम अधूरा पड़ा है।", "Hindi"),
        ("Fluoride contamination in {loc} groundwater is causing health issues.", "English")
    ],
    "environment": [
        ("Factories in {loc} are releasing toxic smoke at night.", "English"),
        ("{loc} ke river mein chemicals dump kiye ja rahe hain.", "Hinglish"),
        ("{loc} में बहुत ज्यादा पेड़ काटे जा रहे हैं, कोई रोक नहीं है।", "Hindi"),
        ("Illegal sand mining is destroying the riverbed in {loc}.", "English"),
        ("Plastic kachra {loc} ke park mein jala rahe hain.", "Hinglish"),
        ("{loc} के पास के जंगल में आग लग गई है, तुरंत बुझाएं।", "Hindi"),
        ("Air quality index in {loc} is hazardous due to construction dust.", "English"),
        ("{loc} mein sound pollution limit se cross ho gaya hai.", "Hinglish"),
        ("पहाड़ों पर {loc} में अवैध खनन हो रहा है।", "Hindi"),
        ("Need proper waste segregation systems in {loc}.", "English")
    ],
    "energy": [
        ("Frequent power cuts in {loc} are affecting student studies.", "English"),
        ("{loc} mein transformer jal gaya hai 3 din pehle.", "Hinglish"),
        ("{loc} में बिजली का बिल बहुत ज्यादा और गलत आ रहा है।", "Hindi"),
        ("Street lights in {loc} sector 4 are not working.", "English"),
        ("High voltage ke karan {loc} mein logo ke TV jal gaye.", "Hinglish"),
        ("हमारे गांव {loc} में अभी तक बिजली के खंभे नहीं लगे हैं।", "Hindi"),
        ("Solar panels installed in {loc} government building are defective.", "English"),
        ("{loc} mein naya meter connection apply kiya tha, abhi tak nahi laga.", "Hinglish"),
        ("बिजली विभाग वाले {loc} में लाइन ठीक करने नहीं आ रहे।", "Hindi"),
        ("Low voltage issue in {loc} is damaging water pumps.", "English")
    ],
    "urban_development": [
        ("The main road in {loc} is full of potholes causing accidents.", "English"),
        ("{loc} mein drainage system block hai, sadak par pani bhara hai.", "Hinglish"),
        ("{loc} में अवैध अतिक्रमण के कारण सड़क जाम रहती है।", "Hindi"),
        ("Construction of the {loc} flyover has been stalled for 2 years.", "English"),
        ("{loc} park mein jhule tute hue hain aur kachra hai.", "Hinglish"),
        ("स्मार्ट सिटी प्रोजेक्ट के तहत {loc} में कोई काम नहीं हुआ।", "Hindi"),
        ("Need public toilets in the busy market area of {loc}.", "English"),
        ("{loc} mein parking ki suvidha nahi hone se traffic jam hota hai.", "Hinglish"),
        ("{loc} में सीवर लाइन का ढक्कन खुला है, खतरा है।", "Hindi"),
        ("Garbage collection truck does not visit {loc} regularly.", "English")
    ],
    "accessibility": [
        ("No wheelchair ramp available at the {loc} railway station.", "English"),
        ("{loc} ke government office mein disabled logo ke liye lift nahi hai.", "Hinglish"),
        ("{loc} के बस स्टैंड पर विकलांगों के लिए कोई सुविधा नहीं है।", "Hindi"),
        ("Blind tactile paths are broken on {loc} footpaths.", "English"),
        ("Divyang pension {loc} mein time par nahi mil rahi hai.", "Hinglish"),
        ("{loc} में मूक-बधिर बच्चों के लिए विशेष स्कूल नहीं है।", "Hindi"),
        ("Public buses in {loc} are not accessible for differently-abled citizens.", "English"),
        ("{loc} hospital mein wheelchair available nahi hai.", "Hinglish"),
        ("विकलांग प्रमाण पत्र बनवाने में {loc} में बहुत दिक्कत आ रही है।", "Hindi"),
        ("Need audio signals at {loc} traffic lights for visually impaired.", "English")
    ],
    "public_admin": [
        ("Bribery is rampant in the {loc} RTO office for driving licenses.", "English"),
        ("{loc} block office mein caste certificate banane mein bahut time lag raha hai.", "Hinglish"),
        ("{loc} में राशन कार्ड में नाम जुड़वाने के लिए पैसे मांगे जा रहे हैं।", "Hindi"),
        ("Online portal for {loc} property tax is continuously crashing.", "English"),
        ("Police verification ke liye {loc} thane mein pareshan kiya ja raha hai.", "Hinglish"),
        ("{loc} के सरकारी बाबू बिना घूस के कोई फाइल पास नहीं करते।", "Hindi"),
        ("Grievance cell phone numbers for {loc} municipality are always switched off.", "English"),
        ("{loc} panchayat mein MNREGA ka payment ruka hua hai.", "Hinglish"),
        ("{loc} तहसील कार्यालय में अधिकारी समय पर नहीं आते।", "Hindi"),
        ("Need better citizen facilitation center in {loc}.", "English")
    ],
    "rural_livelihoods": [
        ("Self-help groups in {loc} are not receiving government funding.", "English"),
        ("{loc} mein MNREGA ke tahat 100 din ka kaam nahi mil raha.", "Hinglish"),
        ("{loc} में कुटीर उद्योग लगाने के लिए कोई सरकारी सहायता नहीं मिल रही है।", "Hindi"),
        ("Skill development center in {loc} has been closed down.", "English"),
        ("{loc} ke gaon mein artisans ko unka saman bechne ka market nahi hai.", "Hinglish"),
        ("{loc} में मुर्गी पालन के लिए सब्सिडी का पैसा नहीं आया।", "Hindi"),
        ("Women weavers in {loc} need micro-loans for purchasing looms.", "English"),
        ("{loc} mein forest produce ka sahi daam nahi mil raha adivasiyon ko.", "Hinglish"),
        ("गांव {loc} से लोग रोजगार की तलाश में पलायन कर रहे हैं।", "Hindi"),
        ("Need modern dairy farming training programs in {loc}.", "English")
    ]
}

data = []
target_per_category = 100  # Total 1000 complaints

for category in categories:
    cat_templates = templates[category]
    for _ in range(target_per_category):
        tmpl, lang = random.choice(cat_templates)
        loc = random.choice(locations)
        complaint_text = tmpl.format(loc=loc)
        
        variation = random.choice(["", " Please help.", " Urgent issue.", " Fix it asap.", " Koi dhyan de.", " Kripya dhyan de."])
        complaint_text += variation
        
        data.append({
            "id": str(uuid.uuid4()),
            "complaint": complaint_text.strip(),
            "category": category,
            "language": lang
        })

random.shuffle(data)

os.makedirs("dataset", exist_ok=True)

with open("dataset/complaints.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["id", "complaint", "category", "language"])
    writer.writeheader()
    for row in data:
        writer.writerow(row)

print(f"Generated {len(data)} complaints successfully at dataset/complaints.csv")
