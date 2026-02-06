import React, { useEffect, useState, createContext } from "react";
import {
	Box,
	Button,
	Container,
	DialogActionTrigger,
	DialogBody,
	DialogContent,
	DialogFooter,
	DialogHeader,
	DialogRoot,
	DialogTitle,
	DialogTrigger,
	Flex,
	Input,
	Stack,
	Text,
} from "@chakra-ui/react";

interface URL {
	id: string;
	item: string;
}

interface UpdateURLProps {
	item: string;
	id: string;
	fetchURLs: () => void;
}

interface DeleteURLProps {
	id: string;
	fetchURLs: () => void;
}

interface URLHelperProps {
	item: string;
	id: string;
	fetchURLs: () => void;
}

const URLsContext = createContext<{
	urls: URL[];
	fetchURLs: () => void;
}>({
	urls: [],
	fetchURLs: () => {},
});

function AddURL() {
	const [item, setItem] = React.useState("");
	const { urls: urls, fetchURLs: fetchURLs } = React.useContext(URLsContext);

	const handleInput = (event: React.ChangeEvent<HTMLInputElement>) => {
		setItem(event.target.value);
	};

	const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
		event.preventDefault();
		const newURL = {
			id: String(urls.length + 1),
			item: item,
		};

		fetch("http://localhost:8000/url", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify(newURL),
		}).then(fetchURLs);
	};

	return (
		<form onSubmit={handleSubmit}>
			<Input
				pr="4.5rem"
				type="text"
				placeholder="Add a URL item"
				aria-label="Add a URL item"
				onChange={handleInput}
			/>
		</form>
	);
}

function URLHelper({ item, id, fetchURLs: fetchURLs }: URLHelperProps) {
	return (
		<Box p={1} shadow="sm">
			<Flex justify="space-between">
				<Text mt={4} as="div">
					{item}
					<Flex align="end">
						<UpdateURL item={item} id={id} fetchURLs={fetchURLs} />
						<DeleteURL id={id} fetchURLs={fetchURLs} />
					</Flex>
				</Text>
			</Flex>
		</Box>
	);
}

const DeleteURL = ({ id, fetchURLs: fetchURLs }: DeleteURLProps) => {
	const deleteURL = async () => {
		await fetch(`http://localhost:8000/url/${id}`, {
			method: "DELETE",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ id: id }),
		});
		await fetchURLs();
	};

	return (
		<Button h="1.5rem" size="sm" marginLeft={2} onClick={deleteURL}>
			Delete URL
		</Button>
	);
};

const UpdateURL = ({ item, id, fetchURLs: fetchURLs }: UpdateURLProps) => {
	const [url, setURL] = useState(item);
	const updateURL = async () => {
		await fetch(`http://localhost:8000/url/${id}`, {
			method: "PUT",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ item: url }),
		});
		await fetchURLs();
	};

	return (
		<DialogRoot>
			<DialogTrigger asChild>
				<Button h="1.5rem" size="sm">
					Update URL
				</Button>
			</DialogTrigger>
			<DialogContent
				position="fixed"
				top="50%"
				left="50%"
				transform="translate(-50%, -50%)"
				bg="white"
				p={6}
				rounded="md"
				shadow="xl"
				maxW="md"
				w="90%"
				zIndex={1000}
			>
				<DialogHeader>
					<DialogTitle>Update URL</DialogTitle>
				</DialogHeader>
				<DialogBody>
					<Input
						pr="4.5rem"
						type="text"
						placeholder="Add a URL item"
						aria-label="Add a URL item"
						value={url}
						onChange={(event) => setURL(event.target.value)}
					/>
				</DialogBody>
				<DialogFooter>
					<DialogActionTrigger asChild>
						<Button variant="outline" size="sm">
							Cancel
						</Button>
					</DialogActionTrigger>
					<Button size="sm" onClick={updateURL}>
						Save
					</Button>
				</DialogFooter>
			</DialogContent>
		</DialogRoot>
	);
};

export default function URLs() {
	const [urls, setURLs] = useState<URL[]>([]);
	const fetchURLs = async () => {
		const response = await fetch("http://localhost:8000/url");
		const urls = await response.json();
		setURLs(urls.data);
	};
	useEffect(() => {
		const loadURLs = async () => {
			const response = await fetch("http://localhost:8000/url");
			const urls = await response.json();
			setURLs(urls.data);
		};
		loadURLs();
	}, []);

	return (
		<URLsContext.Provider value={{ urls: urls, fetchURLs: fetchURLs }}>
			<Container maxW="container.xl" pt="100px">
				<AddURL />
				<Stack gap={5}>
					{urls.map((url) => (
						<URLHelper
							key={url.id}
							item={url.item}
							id={url.id}
							fetchURLs={fetchURLs}
						/>
					))}
				</Stack>
			</Container>
		</URLsContext.Provider>
	);
}
