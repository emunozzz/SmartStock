import axiosClient from "./axiosClient";

/**
 * POST /api/v1/auth/login
 * Confirmado en Swagger: el backend usa el schema Pydantic LoginRequest,
 * que espera JSON con los campos "correo" y "contrasena" (no el form-urlencoded
 * estándar de OAuth2PasswordRequestForm). La respuesta (TokenResponse) trae
 * { access_token, token_type } — sin un objeto "usuario" incluido.
 */
export async function loginRequest({ correo, contrasena }) {
  const { data } = await axiosClient.post("/auth/login", {
    correo,
    contrasena,
  });

  return data; // { access_token, token_type }
}
