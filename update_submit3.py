import re

file_path = "client/src/pages/citizen/SubmitProblem.jsx"
with open(file_path, "r") as f:
    content = f.read()

# Imports
content = content.replace(
    "import { motion } from 'framer-motion';",
    "import { motion, AnimatePresence } from 'framer-motion';\nimport Cropper from 'react-easy-crop';\nimport getCroppedImg from '../../utils/cropImage';"
)

# State
new_state = """  const [step, setStep] = useState(1);

  const [cropModalOpen, setCropModalOpen] = useState(false);
  const [previewModalOpen, setPreviewModalOpen] = useState(false);
  const [imageToCrop, setImageToCrop] = useState(null);
  const [crop, setCrop] = useState({ x: 0, y: 0 });
  const [zoom, setZoom] = useState(1);
  const [croppedAreaPixels, setCroppedAreaPixels] = useState(null);
  const [aspect, setAspect] = useState(1);
"""
content = content.replace("  const [step, setStep] = useState(1);", new_state)

# handleFileUpload
new_file_upload = """  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const url = URL.createObjectURL(file);
      setImageToCrop(url);
      setCropModalOpen(true);
    }
  };

  const onCropComplete = (croppedArea, croppedAreaPixels) => {
    setCroppedAreaPixels(croppedAreaPixels);
  };

  const handleCropConfirm = async () => {
    try {
      const croppedImageFile = await getCroppedImg(imageToCrop, croppedAreaPixels);
      const previewUrl = URL.createObjectURL(croppedImageFile);
      setFormData(prev => ({ ...prev, imageUploaded: true, images: [croppedImageFile], previewUrls: [previewUrl] }));
      setCropModalOpen(false);
      showToast("Image cropped successfully", "success");
    } catch (e) {
      showToast("Failed to crop image", "error");
    }
  };"""
content = re.sub(r'  const handleFileUpload = \(e\) => \{.*?\n  \};\n', new_file_upload + "\n", content, flags=re.DOTALL)

# Add preview modal onClick
content = content.replace(
    '<img src={formData.previewUrls[0]} alt="Preview" className="mx-auto h-32 object-cover rounded-lg" />',
    '<img src={formData.previewUrls[0]} alt="Preview" className="mx-auto h-32 object-cover rounded-lg border border-[#1D3238] shadow-md hover:scale-105 transition-transform" onClick={(e) => { e.preventDefault(); setPreviewModalOpen(true); }} />'
)

# Add Modals at the end of the return
modals = """      {/* Crop Modal */}
      <AnimatePresence>
        {cropModalOpen && (
          <motion.div 
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4"
          >
            <motion.div 
              initial={{ scale: 0.9, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} exit={{ scale: 0.9, opacity: 0 }}
              className="bg-[#16262A] w-full max-w-lg rounded-2xl border border-[#1D3238] overflow-hidden flex flex-col"
            >
              <div className="p-4 border-b border-[#1D3238] flex justify-between items-center bg-[#0F1B1E]">
                <h3 className="font-bold text-[#F2EFE9]">Crop Image</h3>
                <button onClick={() => setCropModalOpen(false)} className="text-[#9BA8A6] hover:text-red-400">✕</button>
              </div>
              
              <div className="relative w-full h-[300px] sm:h-[400px] bg-[#0F1B1E]">
                <Cropper
                  image={imageToCrop}
                  crop={crop}
                  zoom={zoom}
                  aspect={aspect}
                  onCropChange={setCrop}
                  onCropComplete={onCropComplete}
                  onZoomChange={setZoom}
                />
              </div>

              <div className="p-4 space-y-4">
                <div>
                  <label className="text-xs font-mono text-[#9BA8A6] mb-2 block">Zoom</label>
                  <input
                    type="range"
                    value={zoom}
                    min={1}
                    max={3}
                    step={0.1}
                    aria-labelledby="Zoom"
                    onChange={(e) => setZoom(e.target.value)}
                    className="w-full accent-[#E8A33D]"
                  />
                </div>
                
                <div>
                  <label className="text-xs font-mono text-[#9BA8A6] mb-2 block">Aspect Ratio</label>
                  <div className="flex gap-2">
                    <Button variant={aspect === 1 ? 'primary' : 'outline'} className="flex-1 text-xs py-1" onClick={() => setAspect(1)}>1:1 (Square)</Button>
                    <Button variant={aspect === 4/3 ? 'primary' : 'outline'} className="flex-1 text-xs py-1" onClick={() => setAspect(4/3)}>4:3</Button>
                    <Button variant={!aspect ? 'primary' : 'outline'} className="flex-1 text-xs py-1" onClick={() => setAspect(undefined)}>Free Form</Button>
                  </div>
                </div>

                <div className="flex justify-end gap-2 pt-2 border-t border-[#1D3238]">
                  <Button variant="outline" onClick={() => setCropModalOpen(false)}>Cancel</Button>
                  <Button variant="primary" onClick={handleCropConfirm}>Confirm Crop</Button>
                </div>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Preview Modal */}
      <AnimatePresence>
        {previewModalOpen && (
          <motion.div 
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 flex items-center justify-center bg-black/90 p-4"
            onClick={() => setPreviewModalOpen(false)}
          >
            <button className="absolute top-4 right-4 text-white hover:text-red-400 bg-black/50 rounded-full w-10 h-10 flex items-center justify-center backdrop-blur-sm z-50">✕</button>
            <motion.img 
              initial={{ scale: 0.8, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} exit={{ scale: 0.8, opacity: 0 }}
              src={formData.previewUrls[0]} 
              alt="Full Preview" 
              className="max-w-full max-h-full object-contain rounded-lg shadow-2xl"
              onClick={(e) => e.stopPropagation()}
            />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
"""
content = content.replace("    </div>\n  );\n}", modals + "  );\n}")

with open(file_path, "w") as f:
    f.write(content)

print("Updated SubmitProblem.jsx")
