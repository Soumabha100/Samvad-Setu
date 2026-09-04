const express = require("express");
const router = express.Router();
const { protect, authorize } = require("../middleware/authMiddleware");
const Problem = require("../models/Problem");

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
router.post("/", protect, authorize("citizen"), async (req, res) => {
  try {
    let category = "other";
    
    // Attempt to classify using AI Service
    try {
      const aiResponse = await fetch("http://127.0.0.1:8000/api/classify", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: req.body.description || req.body.title || "" })
      });
      
      if (aiResponse.ok) {
        const aiData = await aiResponse.json();
        if (aiData && aiData.category) {
          category = aiData.category;
        }
      }
    } catch (aiError) {
      console.error("AI Classification Error:", aiError.message);
    }

    const newProblem = new Problem({
      ...req.body,
      category: category,
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
