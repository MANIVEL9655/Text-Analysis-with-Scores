# Text-Analysis-with-Scores
## Overview
This project performs text analysis to extract various linguistic metrics, including sentiment scores, readability, and complexity indicators. The analysis includes sentiment classification, personal pronoun detection, and readability scoring.

## Features
- Sentiment Analysis:
  - Positive Score
  - Negative Score
  - Polarity Score
  - Subjectivity Score
- Readability Analysis:
  - Average Sentence Length
  - Percentage of Complex Words
  - Fog Index
  - Syllable per Word
  - Personal Pronoun Count
- Outputs results to an Excel file (`Final_Output.xlsx`)

## Installation
Ensure you have Python installed, then install the required dependencies:

```bash
pip install requests beautifulsoup4 pandas textblob nltk openpyxl
```

## Usage
1. Place `Input.xlsx`, `positive-words.txt`, and `negative-words.txt` in the project directory.
2. Run the script:

   ```bash
   python script.py
   ```

3. The output file `Final_Output.xlsx` will be generated with the computed metrics.

## Input Files
- `Input.xlsx`: Contains the text data to be analyzed.
- `positive-words.txt`: List of positive words for sentiment analysis.
- `negative-words.txt`: List of negative words for sentiment analysis.

## Output Format
The script outputs a structured Excel file (`Final_Output.xlsx`) with the following columns:
- **URL_ID**
- **Positive Score**
- **Negative Score**
- **Polarity Score**
- **Subjectivity Score**
- **Avg Sentence Length**
- **Percentage of Complex Words**
- **Fog Index**
- **Avg Number of Words per Sentence**
- **Complex Word Count**
- **Word Count**
- **Syllable per Word**
- **Personal Pronouns**
- **Avg Word Length**

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with improvements or bug fixes.
