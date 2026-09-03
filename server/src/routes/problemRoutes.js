const express = require("express");
const router = express.Router();
const { protect, authorize } = require("../middleware/authMiddleware");
const Problem = require("../models/Problem");
const { upload, uploadToCloudinary } = require("../middleware/upload");
const cloudinary = require("../config/cloudinary");

// Public Route: Anyone can view public problems
router.get("/public", async (req, res) => {
  try {
    const problems = await Problem.find().populate("reportedBy", "name").sort({ createdAt: -1 });
    res.json(problems);
  } catch (error) {
    res.status(500).json({ message: "Server Error", error: error.message });
  }
});

// Role-Restricted Route: Only 'citizen' can submit a problem
router.post("/", protect, authorize("citizen"), upload.array('images', 3), async (req, res) => {
  try {
    let location = req.body.location;
    if (typeof location === 'string') {
      location = JSON.parse(location);
    }

    const uploadedImages = [];
    if (req.files && req.files.length > 0) {
      for (const file of req.files) {
        const result = await uploadToCloudinary(file.buffer);
        uploadedImages.push({
          url: result.secure_url,
          publicId: result.public_id,
        });
      }
    }

    const newProblem = new Problem({
      ...req.body,
      location,
      images: uploadedImages,
      reportedBy: req.user._id,
      timeline: [
        { stage: "Reported", timestamp: "Just now", actor: "Citizen" },
        { stage: "Classified", timestamp: "Just now", actor: "AI Engine" }
      ]
    });
    const savedProblem = await newProblem.save();
    res.status(201).json(savedProblem);
  } catch (error) {
    res.status(500).json({ message: "Server Error", error: error.message });
  }
});

// Role-Restricted Route: Only 'citizen' can delete their own problem
router.delete("/:id", protect, authorize("citizen"), async (req, res) => {
  try {
    const problem = await Problem.findOne({ _id: req.params.id, reportedBy: req.user._id });
    if (!problem) {
      return res.status(404).json({ message: "Problem not found or unauthorized to delete" });
    }
    
    // Delete images from Cloudinary
    if (problem.images && problem.images.length > 0) {
      for (const image of problem.images) {
        if (image.publicId) {
          await cloudinary.uploader.destroy(image.publicId);
        }
      }
    }

    await Problem.findByIdAndDelete(req.params.id);
    res.json({ message: "Problem deleted successfully" });
  } catch (error) {
    res.status(500).json({ message: "Server Error", error: error.message });
  }
});

// Role-Restricted Route: Only 'hei' or 'hei_admin' can claim problems
router.post(
  "/:id/claim",
  protect,
  authorize("hei", "hei_admin"),
  async (req, res) => {
    res.json({ message: "Problem claimed by institution" });
  },
);

// Role-Restricted Route: Only 'government_admin' or 'govt_admin' can moderate
router.patch(
  "/:id/moderate",
  protect,
  authorize("government_admin", "govt_admin", "platform_admin"),
  async (req, res) => {
    res.json({ message: "Problem status updated by admin" });
  },
);

module.exports = router;
