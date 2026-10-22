// Prototipo de referencia visual. Tokens provisionales de DESIGN.md.
const t = {
  primary: "#8B1E2D", primaryDark: "#6E1824", accent: "#FFC000",
  bg: "#FFFFFF", surface: "#F7F5F2", border: "#E5E0DA",
  text: "#1F1F1F", muted: "#6B6B6B", success: "#2E7D32", error: "#B3261E",
};
const boton = { minHeight: 48, fontSize: 18, fontWeight: 600, borderRadius: 8, padding: "0 24px", cursor: "pointer" };
const primario = { ...boton, background: t.primary, color: "#fff", border: "none" };
const tarjeta = { background: t.surface, border: `1px solid ${t.border}`, borderRadius: 12, padding: 24 };

export default function Catalogo() {
  return (
    <main style={{ background: t.bg, color: t.text, fontSize: 16, padding: 32, minHeight: "100vh" }}>
      <h1 style={{ fontSize: 28 }}>Catálogo</h1>
      <input aria-label="Buscar libro" placeholder="Título, autor o ISBN" style={{ minHeight: 48, fontSize: 18, width: "100%", maxWidth: 480 }} />
      <ul style={{ listStyle: "none", padding: 0, display: "grid", gap: 16, gridTemplateColumns: "repeat(auto-fill, minmax(240px, 1fr))" }}>
        <li style={tarjeta}>
          <h2 style={{ fontSize: 20 }}>Título del libro</h2>
          <p style={{ color: t.muted }}>Autor · 2 ejemplares disponibles</p>
          <span style={{ color: t.success }}>✔ Disponible</span>
        </li>
      </ul>
    </main>
  );
}
