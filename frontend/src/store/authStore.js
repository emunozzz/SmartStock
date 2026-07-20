import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";

/**
 * Store global de autenticación.
 *
 * Usamos Zustand + persist para:
 *  1. Mantener la sesión activa tras un refresh de página (persistido en localStorage).
 *  2. Exponer el token de forma síncrona a axiosClient (fuera de React,
 *     mediante useAuthStore.getState()), sin necesidad de Context/Providers.
 *
 * Nota de seguridad: localStorage es vulnerable a XSS. Es el estándar para
 * proyectos académicos/MVP como este; en un entorno productivo real se
 * recomendaría httpOnly cookies emitidas por el backend.
 */
export const useAuthStore = create(
  persist(
    (set) => ({
      token: null,
      usuario: null, // { usuario_id, nombre, rol, ... } según lo que devuelva /auth/login
      isAuthenticated: false,

      login: ({ access_token, usuario }) =>
        set({
          token: access_token,
          usuario: usuario ?? null,
          isAuthenticated: true,
        }),

      logout: () =>
        set({
          token: null,
          usuario: null,
          isAuthenticated: false,
        }),
    }),
    {
      name: "smartstock-auth", // key en localStorage
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({
        token: state.token,
        usuario: state.usuario,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);
