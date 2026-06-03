type Props = {
  label: string;
  value: string;
  tone?: "teal" | "coral" | "violet" | "amber";
};

export default function MetricCard({ label, value, tone = "teal" }: Props) {
  return (
    <article className={`metric-card ${tone}`}>
      <span>{label}</span>
      <strong>{value}</strong>
    </article>
  );
}
