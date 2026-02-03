import { ChakraProvider } from "@chakra-ui/react";
import { defaultSystem } from "@chakra-ui/react";
import Header from "./components/Header";
import URLs from "./components/URLs";

function App() {
	return (
		<ChakraProvider value={defaultSystem}>
			<Header />
			<URLs />
		</ChakraProvider>
	);
}

export default App;
