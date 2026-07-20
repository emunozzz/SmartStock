import axiosClient from "./axiosClient";

export async function listarVentas() {
  const { data } = await axiosClient.get("/ventas/");
  return data;
}

export async function registrarVenta({ cliente_id, detalles }) {
  const { data } = await axiosClient.post("/ventas/", {
    cliente_id,
    detalles,
  });
  return data;
}
