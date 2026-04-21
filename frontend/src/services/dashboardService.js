import API from "./api";

export const getDashboardData = async () => {
  const res = await API.get("/dashboard/");
  return res.data;
};