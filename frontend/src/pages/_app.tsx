import "@/styles/globals.css";
import type { AppProps } from "next/app";
import React from "react";
import { ChakraProvider, Box } from "@chakra-ui/react";
import WithSubnavigation from "../../components/Navbar";

export default function App({ Component, pageProps }: AppProps) {
  return (
    <ChakraProvider>
      <Box bg={"gray.100"} minHeight="100vh">
        <WithSubnavigation />
        <Component {...pageProps} />
      </Box>
    </ChakraProvider>
  );
}
