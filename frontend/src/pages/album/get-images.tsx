import { useEffect, useState } from "react";
import ImageGallery from "../../../components/ImageGallery";
import axios from "axios";

type ImageFile = {
  filename: string;
  base64: string;
};

type FolderStructure = {
  [key: string]: {
    files: ImageFile[];
  };
};

const IndexPage: React.FC = () => {
  const [data, setData] = useState<FolderStructure | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // APIから画像データを取得
    const fetchData = async () => {
      try {
        const baseUrl = `${window.location.protocol}//${window.location.hostname}:8000`;
        const response = await axios.get(`${baseUrl}/get-images/`);
        if (!response) {
          throw new Error("Failed to fetch images");
        }
        const result: FolderStructure = response.data;
        console.log(result)
        setData(result);
      } catch (error) {
        setError((error as Error).message);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div>
      <h1>Image Gallery</h1>
      {data ? (
        Object.entries(data).map(([folderName, folderData]) => (
          <ImageGallery
            key={folderName}
            folderName={folderName}
            images={folderData.files}
          />
        ))
      ) : (
        <p>No images available</p>
      )}
    </div>
  );
};

export default IndexPage;
