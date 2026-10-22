// Prototipo de referencia visual. Tokens provisionales de DESIGN.md.
const t = {
  primary: "#8B1E2D", primaryDark: "#6E1824", accent: "#FFC000",
  bg: "#FFFFFF", surface: "#F7F5F2", border: "#E5E0DA",
  text: "#1F1F1F", muted: "#6B6B6B", success: "#2E7D32", error: "#B3261E",
};
const boton = { minHeight: 48, fontSize: 18, fontWeight: 600, borderRadius: 8, padding: "0 24px", cursor: "pointer" };
const primario = { ...boton, background: t.primary, color: "#fff", border: "none" };
const tarjeta = { background: t.surface, border: `1px solid ${t.border}`, borderRadius: 12, padding: 24 };

export default function Login() {
  return (
    <main style={{ background: t.bg, color: t.text, fontSize: 16, padding: 32, minHeight: "100vh" }}>
      <section style={{ ...tarjeta, maxWidth: 420, margin: "0 auto" }}>
        <h1 style={{ fontSize: 28 }}>Iniciar sesión</h1>
        <label htmlFor="correo">Correo institucional</label>
        <input id="correo" type="email" style={{ display: "block", width: "100%", minHeight: 48, fontSize: 18, marginBottom: 16 }} />
        <label htmlFor="clave">Contraseña</label>
        <input id="clave" type="password" style={{ display: "block", width: "100%", minHeight: 48, fontSize: 18, marginBottom: 24 }} />
        <button style={primario}>Entrar</button>
      </section>
    </main>
  );
}
