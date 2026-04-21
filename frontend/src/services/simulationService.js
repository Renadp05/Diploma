import API from "./api";

export const getCompareSimulation = async () => {
  const res = await API.get("/simulation/compare");
  return res.data;
};