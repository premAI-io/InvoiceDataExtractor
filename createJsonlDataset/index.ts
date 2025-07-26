import { readdir, readFile, appendFile } from "fs/promises";
import { join } from "path";
import PremAI from "@premai/premai";

const client = new PremAI({
  apiKey: process.env["PREMAI_API_KEY"],
});

const systemPrompt = `
You are a helpful assistant that can extract informations from invoices that have been converted to markdown.

The user will provide you with a markdown file.

Please extract the following informations:

- datetime
- total amount
- currency
- name of the business
- location of the business (city, state, country)


return the informations in a json format like this:

{
    "datetime": "2021-01-01 12:00:00",
    "total_amount": 132.56,
    "currency": "USD",
    "business_name": "Business Name",
    "business_location": "City, State, Country"
}

If you don't find the informations, return null for the corresponding field. If no information is found, return null for all fields.

Your response should be only the json object, no other text or comments, and no markdown formatting (no \`\`\`json or \`\`\`).
`;

async function processInvoiceFiles() {
  // Read the mdData directory
  const mdDataPath = join(process.cwd(), "..", "dataset", "mdData");
  const files = await readdir(mdDataPath);

  // Filter for .md files and take first 5
  const mdFiles = files.filter((file) => file.endsWith(".md"));

  console.log(
    `Processing first ${mdFiles.length} files from mdData directory:\n`,
  );

  const outputPath = join(process.cwd(), "invoiceDataset.jsonl");
  let savedCount = 0;

  // Process each file
  for (const [index, fileName] of mdFiles.entries()) {
    if (!fileName) continue;

    const filePath = join(mdDataPath, fileName);

    try {
      const content = await readFile(filePath, "utf-8");
      const title = fileName.replace(".md", "");

      const userPrompt = `(original: ${title}.pdf markdown: ${title}.md) ${content}`;

      console.log(`=== Processing File ${index + 1}: ${title} ===`);

      // Call PremAI to extract invoice information
      const response = await client.chat.completions({
        messages: [
          { role: "system", content: systemPrompt },
          { role: "user", content: userPrompt },
        ],
        model: "claude-4-sonnet",
      });

      const extractedData = response.choices?.[0]?.message?.content;
      if (extractedData) {
        console.log("Extracted data:", extractedData);

        // Create conversation object in the required format
        const conversation = {
          messages: [
            { role: "system", content: systemPrompt },
            { role: "user", content: userPrompt },
            { role: "assistant", content: extractedData },
          ],
        };

        // Append to JSONL file immediately
        const jsonLine = JSON.stringify(conversation) + "\n";
        await appendFile(outputPath, jsonLine, "utf-8");
        savedCount++;

        console.log(
          `✅ Saved conversation ${savedCount} to invoiceDataset.jsonl`,
        );
      } else {
        console.log("No data extracted");
      }
      console.log("---\n");
    } catch (error) {
      console.error(`Error processing file ${fileName}:`, error);
    }
  }

  console.log(`\n🎉 Total conversations saved: ${savedCount}`);
}

// Run the function
processInvoiceFiles();
