import axiosClient from "./axiosClient";

export async function listarCompras() {
  const { data } = await axiosClient.get("/compras/");
  return data;
}
