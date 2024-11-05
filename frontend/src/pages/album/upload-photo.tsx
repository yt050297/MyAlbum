import React, { useState } from "react";
import {
  Box,
  Button,
  Input,
  Stack,
  Container,
  Heading,
  Text,
  Img,
} from "@chakra-ui/react";
import axios from "axios";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

const UploadPhoto = () => {
  const [file, setFile] = useState<string | null>(null);
  const [previewSrc, setPreviewSrc] = useState<string | null>(null); // 画像のプレビュー用
  const [message, setMessage] = useState<string | null>(null);
  const [errors, setErrors] = useState<any | null>(null);
  const [albumTitle, setAlbumTitle] = useState<string>("");
  const [selectedDate, setSelectedDate] = useState<Date | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0] || null;
    if (selectedFile) {
      const reader = new FileReader();
      reader.onloadend = () => {
        const base64String = reader.result?.toString().split(",")[1];
        setFile(base64String || null);
        setPreviewSrc(reader.result?.toString() || null); // プレビュー画像用にBase64をセット
      };
      reader.readAsDataURL(selectedFile);
    }
  };

  const handleUpload = async () => {
    if (!file || !albumTitle || !selectedDate) {
      setErrors("All fields are required");
      return;
    } else {
      setErrors(null);
    }

    const jsonData = {
      title: albumTitle,
      album_date: selectedDate.toISOString().split("T")[0], // YYYY-MM-DD形式
      file: file,
    };
    const baseUrl = `${window.location.protocol}//${window.location.hostname}:8000`;

    try {
      const response = await axios.post(`${baseUrl}/upload-image/`, jsonData, {
        headers: { "Content-Type": "application/json" },
      });
      if (response.data.result === "false") {
        // バリデーションエラーメッセージをセットする
        setErrors(
          response.data.errors
            .map((error: any) => `${error.loc[1]}: ${error.msg}`)
            .join(", ")
        );
      } else {
        setMessage(response.data.message);
      }
    } catch (error: any) {
      // バックエンドからのエラーメッセージを取得して表示
      if (error.response) {
        setErrors(JSON.stringify(error.response.data.detail, null, 2));
        console.log("Error response:", error.response.data.detail);
      } else {
        setErrors("Error uploading file");
      }
      setMessage(null);
    }
  };

  return (
    <Container
      maxW={"container.md"}
      display="flex"
      justifyContent="center"
      alignItems="center"
      minHeight="80vh"
    >
      <Stack
        bg={"gray.50"}
        rounded={"xl"}
        boxShadow={"2xl"}
        p={{ base: 4, sm: 6, md: 8 }}
        spacing={{ base: 8 }}
        m={4}
      >
        <Stack spacing={4}>
          <Heading
            color={"gray.800"}
            lineHeight={1.1}
            fontSize={{ base: "2xl", sm: "3xl", md: "4xl" }}
          >
            Upload your photo
            <Text
              as={"span"}
              bgGradient="linear(to-r, red.400,pink.400)"
              bgClip="text"
            >
              !
            </Text>
          </Heading>
          <Text color={"gray.500"} fontSize={{ base: "sm", sm: "md" }}>
            Please upload your photo here. You can select multiple photos here.
          </Text>
        </Stack>
        <Box mt={4}>
          <Stack spacing={4}>
            {errors && (
              <Box mt={6} color={"red"}>
                <Text>{errors}</Text>
              </Box>
            )}
            <Input
              placeholder="Title of album"
              bg={"gray.100"}
              border={0}
              color={"gray.500"}
              _placeholder={{
                color: "gray.500",
              }}
              value={albumTitle}
              onChange={(e) => setAlbumTitle(e.target.value)}
            />
            <DatePicker
              selected={selectedDate}
              onChange={(date: Date | null) => setSelectedDate(date)}
              customInput={
                <Input bg={"gray.100"} border={0} color={"gray.500"} />
              }
              placeholderText="Select a date"
              dateFormat={"yyyy/MM/dd"}
            />
            <Input
              pt={1}
              type="file"
              fontFamily={"heading"}
              bg={"gray.200"}
              color={"gray.800"}
              onChange={handleFileChange}
            />
            {previewSrc && (
              <Box>
                <Text>Image Preview:</Text>
                <Img
                  src={previewSrc}
                  alt="Selected Image Preview"
                  style={{ maxHeight: "300px" }}
                />
              </Box>
            )}
          </Stack>
          <Button
            fontFamily={"heading"}
            mt={8}
            w={"full"}
            bgGradient="linear(to-r, red.400,pink.400)"
            color={"white"}
            _hover={{
              bgGradient: "linear(to-r, red.400,pink.400)",
              boxShadow: "xl",
            }}
            onClick={handleUpload}
          >
            Submit
          </Button>
        </Box>
        {message && (
          <Box mt={6} color={"red"}>
            <Text>{message}</Text>
          </Box>
        )}
      </Stack>
    </Container>
  );
};

export default UploadPhoto;
