import API from "./api";

export const getRiskAnalysis = async (txId, walletAddress) => {
  const res = await API.get(`/tx/${txId}/risk-analysis`, {
    params: { wallet_address: walletAddress },
  });

  return res.data;
};