package com.example.bosch;

import java.util.Map;

import org.springframework.ai.azure.openai.AzureOpenAiChatClient;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestClient;

@SpringBootApplication
@RestController
public class BoschApplication {

	@Autowired
	AzureOpenAiChatClient azureOpenAiChatClient;

	@GetMapping
	public Map hello() {

		RestClient restClient = RestClient.create();

		String year = restClient.get().uri("http://localhost:5000").retrieve().body(String.class);

		String prompt = """

			Dear machine, please give me a random movie quote from the year %s
		
		""".formatted(year);

		return Map.of(prompt,azureOpenAiChatClient.call(prompt));
	}

	public static void main(String[] args) {
		SpringApplication.run(BoschApplication.class, args);
	}

}
