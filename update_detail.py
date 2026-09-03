import re

file_path = "client/src/pages/public/ProblemDetail.jsx"
with open(file_path, "r") as f:
    content = f.read()

# Imports
content = content.replace(
    "import { useParams, Link, useNavigate } from 'react-router-dom';",
    "import { useParams, Link, useNavigate } from 'react-router-dom';\nimport { motion, AnimatePresence } from 'framer-motion';"
)

# State
content = content.replace(
    "  const [problem, setProblem] = useState(null);",
    "  const [problem, setProblem] = useState(null);\n  const [previewImage, setPreviewImage] = useState(null);"
)

# Redesign attached evidence section
new_evidence_section = """            {/* Uploaded Media Display */}
            <div className="bg-[#16262A] p-6 rounded-xl border border-[#1D3238] space-y-4 shadow-lg">
              <h3 className="text-sm font-bold font-display flex items-center gap-2">
                <Camera size={18} className="text-[#E8A33D]" /> Attached Evidence
              </h3>
              {problem.images && problem.images.length > 0 ? (
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                  {problem.images.map((img, idx) => (
                    <motion.div 
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                      key={idx}
                      className="cursor-pointer rounded-lg overflow-hidden border-2 border-transparent hover:border-[#E8A33D] transition-colors shadow-sm aspect-square relative group"
                      onClick={() => setPreviewImage(img.url)}
                    >
                      <img 
                        src={img.url} 
                        alt={`Evidence ${idx + 1}`} 
                        className="w-full h-full object-cover" 
                      />
                      <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                        <span className="text-white text-xs font-mono font-bold bg-black/60 px-2 py-1 rounded backdrop-blur-sm">View Full</span>
                      </div>
                    </motion.div>
                  ))}
                </div>
              ) : (
                <div className="p-8 border-2 border-dashed border-[#1D3238] rounded-xl bg-[#0F1B1E] flex flex-col items-center justify-center text-[#9BA8A6]">
                  <Camera size={36} className="mb-3 opacity-30" />
                  <p className="text-sm font-medium">No evidence photos attached</p>
                </div>
              )}
            </div>"""

content = re.sub(
    r'\{/\* Uploaded Media Display \*/\}.*?(?=          </div>\n\n          \{/\* Life Cycle Audit Timeline)',
    new_evidence_section + "\n",
    content,
    flags=re.DOTALL
)

# Add Preview Modal at the bottom
preview_modal = """
      {/* Full Screen Image Preview Modal */}
      <AnimatePresence>
        {previewImage && (
          <motion.div 
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 flex items-center justify-center bg-black/90 backdrop-blur-md p-4"
            onClick={() => setPreviewImage(null)}
          >
            <button className="absolute top-6 right-6 text-white hover:text-red-400 bg-[#1D3238]/50 hover:bg-[#1D3238] rounded-full w-12 h-12 flex items-center justify-center backdrop-blur-sm transition-all z-50 shadow-lg border border-white/10">
              <span className="text-xl leading-none -mt-0.5">✕</span>
            </button>
            <motion.img 
              initial={{ scale: 0.8, y: 20, opacity: 0 }} animate={{ scale: 1, y: 0, opacity: 1 }} exit={{ scale: 0.8, y: 20, opacity: 0 }}
              transition={{ type: "spring", bounce: 0.35 }}
              src={previewImage} 
              alt="Full Preview" 
              className="max-w-full max-h-[90vh] object-contain rounded-xl shadow-[0_0_50px_rgba(0,0,0,0.5)] border border-white/10"
              onClick={(e) => e.stopPropagation()}
            />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
"""
content = content.replace("    </div>\n  );\n}", preview_modal + "  );\n}")

with open(file_path, "w") as f:
    f.write(content)

print("Updated ProblemDetail.jsx")
