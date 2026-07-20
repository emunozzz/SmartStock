export default function KpiCard({ label, value, hint, tone = "default" }) {
  const toneStyles = {
    default: "text-slate-900",
    positive: "text-emerald-600",
    warning: "text-amber-600",
    critical: "text-red-600",
  };

  return (
    <div className="bg-white border border-slate-200 rounded-2xl shadow-sm p-5">
      <p className="text-xs font-medium text-slate-500">{label}</p>
      <p className={`text-2xl font-semibold mt-2 ${toneStyles[tone]}`}>
        {value}
      </p>
      {hint && <p className="text-xs text-slate-400 mt-1">{hint}</p>}
    </div>
  );
}
