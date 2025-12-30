import { ChakraProvider } from '@chakra-ui/react'
import { defaultSystem } from "@chakra-ui/react"
import Header from "./components/Header";
import Todos from "./components/Todos";  // new

function App() {
  console.log("bla")
  return (
    <ChakraProvider value={defaultSystem}>
      <Header />
      <Todos />
    </ChakraProvider>
  )
}

export default App;
