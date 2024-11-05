import type { NextApiRequest, NextApiResponse } from "next";

const mockData = {
  ".": {
    files: [],
  },
  "album-2024-10-13": {
    files: [
      {
        filename: "album_1728906744.546094.jpeg",
        base64: "data:image/jpeg;base64,...",
      },
      {
        filename: "album_1728905556.920942.jpeg",
        base64: "data:image/jpeg;base64,...",
      },
    ],
  },
  "記念-2024-10-21": {
    files: [
      {
        filename: "記念_1729692826.005752.jpeg",
        base64: "data:image/jpeg;base64,...",
      },
    ],
  },
};

export default function handler(req:NextApiRequest, res:NextApiResponse){
  res.status(200).json(mockData);
}