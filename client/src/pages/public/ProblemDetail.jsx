import React, { useEffect, useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { MapPin, Calendar, Building2, ShieldCheck, ArrowLeft, Award, Sparkles, CheckCircle2, Trash2, Camera } from 'lucide-react';
import { useAuthStore } from '../../store/authStore';
import { useProblemStore } from '../../store/problemStore';
import { useToastStore } from '../../store/toastStore';
import SignalDot from '../../components/ui/SignalDot';
import Badge from '../../components/ui/Badge';
import Button from '../../components/ui/Button';

export default function ProblemDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { problems, fetchProblems, deleteProblem } = useProblemStore();
  const { user } = useAuthStore();
  const { showToast } = useToastStore();
  const [problem, setProblem] = useState(null);
  const [previewImage, setPreviewImage] = useState(null);

  const handleDelete = async () => {
    if (window.confirm("Are you sure you want to delete this problem?")) {
      const success = await deleteProblem(id);
      if (success) {
        showToast("Problem deleted successfully.", "success");
        navigate('/citizen/dashboard');
      }
    }
  };

  useEffect(() => {
    if (problems.length === 0) {
      fetchProblems();
    } else {
      const found = problems.find((p) => p.id === id);
      setProblem(found || problems[0]); // Fallback to first problem if direct ID match isn't found
    }
  }, [id, problems]);

  if (!problem) {
    return (
      <div className="min-h-screen bg-[#0F1B1E] text-[#F2EFE9] flex items-center justify-center">
        <p className="text-[#9BA8A6]">Loading problem details...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0F1B1E] text-[#F2EFE9] p-6 max-w-5xl mx-auto space-y-8">
      {/* Top Header & Navigation */}
      <div className="flex items-center justify-between border-b border-[#1D3238] pb-4">
        <Link 
          to={(() => {
            const role = user?.role;
            if (role === "hei" || role === "hei_admin") return "/hei/dashboard";
            if (role === "industry_csr" || role === "industry_admin") return "/industry/dashboard";
            if (role === "government_admin" || role === "admin" || role === "govt_admin" || role === "platform_admin") return "/admin/analytics";
            return "/citizen/dashboard";
          })()}
          className="inline-flex items-center gap-2 text-xs font-mono text-[#9BA8A6] hover:text-[#F2EFE9] transition-colors"
        >
          <ArrowLeft size={16} /> Back to Dashboard
        </Link>
        <span className="text-xs font-mono text-[#E8A33D] bg-[#E8A33D]/10 px-2 py-1 rounded">
          ID: {problem.id}
        </span>
      </div>

      <div className="grid md:grid-cols-3 gap-8">
        {/* Left 2 Columns: Details & Timeline */}
        <div className="md:col-span-2 space-y-8">
          {/* Main Title & Overview */}
          <div className="space-y-4">
            <div className="flex items-center gap-3">
              <SignalDot status={problem.status} size="lg" />
              <Badge status={problem.status} />
              <span className="text-xs font-mono text-[#9BA8A6]">
                Urgency: <strong className="text-[#E8A33D] uppercase">{problem.urgency || 'Medium'}</strong>
              </span>
            </div>

            <div className="flex items-center justify-between">
              <h1 className="text-3xl font-bold font-display">{problem.title}</h1>
              {user && (user.id === problem.reportedBy?._id || user.id === problem.reportedBy?.id || user.id === problem.reportedBy) && (
                <Button 
                  variant="outline" 
                  className="border-red-900/50 text-red-400 hover:bg-red-400/10 hover:border-red-400 flex items-center gap-2 text-xs py-2 px-3" 
                  onClick={handleDelete}
                >
                  <Trash2 size={14} /> Delete
                </Button>
              )}
            </div>

            <div className="flex flex-wrap items-center gap-4 text-xs text-[#9BA8A6]">
              <span className="flex items-center gap-1">
                <MapPin size={14} className="text-[#E8A33D]" /> {problem.location?.district || "Jharkhand"}, {problem.location?.block || "Block"}
              </span>
              <span className="flex items-center gap-1">
                <Calendar size={14} /> Reported on {new Date(problem.createdAt || Date.now()).toLocaleDateString()}
              </span>
            </div>

            <p className="text-sm text-[#9BA8A6] leading-relaxed bg-[#16262A] p-4 rounded-xl border border-[#1D3238]">
              {problem.description}
            </p>

                        {/* Uploaded Media Display */}
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
            </div>
          </div>

          {/* Life Cycle Audit Timeline (Section 3.7) */}
          <div className="space-y-4 bg-[#16262A] p-6 rounded-xl border border-[#1D3238]">
            <h2 className="text-lg font-bold font-display flex items-center gap-2">
              <Sparkles size={18} className="text-[#2F9E8F]" /> Resolution Audit Timeline
            </h2>

            <div className="relative border-l-2 border-[#1D3238] ml-3 pl-6 space-y-6">
              {(problem.timeline || [
                { stage: "Reported", timestamp: "Recent", actor: "Citizen" },
                { stage: "Classified", timestamp: "Recent", actor: "AI Engine" }
              ]).map((item, index) => (
                <div key={index} className="relative space-y-1">
                  {/* Timeline Dot */}
                  <div className="absolute -left-[31px] top-1 w-3 h-3 rounded-full bg-[#2F9E8F] border-4 border-[#0F1B1E]" />
                  <div className="flex items-center justify-between">
                    <h4 className="text-sm font-bold text-[#F2EFE9]">{item.stage}</h4>
                    <span className="text-xs font-mono text-[#9BA8A6]">{item.timestamp}</span>
                  </div>
                  <p className="text-xs text-[#9BA8A6]">Action performed by: <span className="text-[#E8A33D]">{item.actor}</span></p>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Right Column: Institutional Ownership & Role Actions */}
        <div className="space-y-6">
          {/* Assigned HEI Card */}
          <div className="bg-[#16262A] p-6 rounded-xl border border-[#1D3238] space-y-4">
            <h3 className="text-xs font-mono text-[#9BA8A6] uppercase tracking-wider">Assigned Technical Partner</h3>
            {problem.assignedInstitution ? (
              <div className="space-y-3">
                <div className="flex items-start gap-3">
                  <Building2 size={24} className="text-[#2F9E8F] shrink-0 mt-1" />
                  <div>
                    <h4 className="text-sm font-bold">{problem.assignedInstitution}</h4>
                    <p className="text-xs text-[#9BA8A6]">Verification status: Verified HEI</p>
                  </div>
                </div>
                <div className="p-3 bg-[#0F1B1E] rounded-lg border border-[#1D3238] text-xs space-y-1">
                  <p className="text-[#9BA8A6]">Project Lead: <strong className="text-[#F2EFE9]">Student Team Alpha</strong></p>
                  <p className="text-[#9BA8A6]">Faculty Advisor: <strong className="text-[#F2EFE9]">Dr. A. Sharma</strong></p>
                </div>
              </div>
            ) : (
              <div className="space-y-3 text-center py-2">
                <p className="text-xs text-[#9BA8A6]">Unclaimed by higher educational institutions.</p>
                <Link to="/signup?role=university">
                  <Button variant="outline" className="w-full text-xs py-2">Claim as University</Button>
                </Link>
              </div>
            )}
          </div>

          {/* CSR Support Card */}
          <div className="bg-[#16262A] p-6 rounded-xl border border-[#1D3238] space-y-4">
            <h3 className="text-xs font-mono text-[#9BA8A6] uppercase tracking-wider">CSR Sponsorship</h3>
            <div className="space-y-3">
              <div className="flex items-center justify-between text-xs">
                <span className="text-[#9BA8A6]">Required Budget:</span>
                <span className="font-mono font-bold text-[#E8A33D]">₹45,000</span>
              </div>
              <div className="flex items-center justify-between text-xs">
                <span className="text-[#9BA8A6]">Pledged So Far:</span>
                <span className="font-mono font-bold text-[#2F9E8F]">₹15,000</span>
              </div>
              <Link to="/signup?role=industry">
                <Button variant="secondary" className="w-full text-xs py-2 mt-2">
                  <Award size={14} /> Pledge CSR Funds
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </div>

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
  );
}