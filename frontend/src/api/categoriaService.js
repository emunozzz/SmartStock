import axiosClient from "./axiosClient";

export async function listarCategorias() {
  const { data } = await axiosClient.get("/categorias/");
  return data;
}
