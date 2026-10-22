// Prototipo de referencia visual. Tokens provisionales de DESIGN.md.
const t = {
  primary: "#8B1E2D", primaryDark: "#6E1824", accent: "#FFC000",
  bg: "#FFFFFF", surface: "#F7F5F2", border: "#E5E0DA",
  text: "#1F1F1F", muted: "#6B6B6B", success: "#2E7D32", error: "#B3261E",
};
const boton = { minHeight: 48, fontSize: 18, fontWeight: 600, borderRadius: 8, padding: "0 24px", cursor: "pointer" };
const primario = { ...boton, background: t.primary, color: "#fff", border: "none" };
const tarjeta = { background: t.surface, border: `1px solid ${t.border}`, borderRadius: 12, padding: 24 };

export default function Multas() {
  return (
    <main style={{ background: t.bg, color: t.text, fontSize: 16, padding: 32, minHeight: "100vh" }}>
      <h1 style={{ fontSize: 28 }}>Cobro de multa</h1>
      <section style={tarjeta}>
        <p style={{ fontSize: 18 }}>Usuario: Nombre Apellido</p>
        <p style={{ fontSize: 18 }}>Monto a cobrar: <strong>$0.00</strong></p>
        <p style={{ color: t.error }}>⚠ El cobro no se puede deshacer.</p>
        <button style={primario}>Confirmar cobro</button>
      </section>
    </main>
  );
}
