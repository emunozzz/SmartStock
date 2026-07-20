import axiosClient from "./axiosClient";

export async function listarClientes() {
  const { data } = await axiosClient.get("/clientes/");
  return data;
}
