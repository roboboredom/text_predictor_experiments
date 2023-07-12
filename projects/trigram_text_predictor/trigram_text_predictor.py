from collections import defaultdict
from itertools import islice
import random, time, os, re


def build_bigram_model(text):
	"""
	Build a bigram model from the input text.
	
	Args:
		text (str): The input text.
	
	Returns:
		dict: The bigram model as a nested dictionary.
	"""
	# Tokenize the input text by splitting on both whitespace and punctuation characters
	# The regular expression [\w']+ matches sequences of word characters and apostrophes 
	# (to capture contractions as single tokens) The regular expression [.,!?;:] matches 
	# common punctuation characters. Using findall with these combined expressions 
	# returns a list of tokens split on both whitespace and punctuation.
	#tokenized_text = re.findall(r"[\w']+|[.,!?;:]", text)
	def split_string_and_whitespace(string, n):
		tokens = []
		current_token = ""
		for char in string:
			if char.isspace():
				if current_token:
					tokens.append(current_token)
					current_token = ""
				tokens.append(char)
			else:
				current_token += char
				if len(current_token) == n:
					tokens.append(current_token)
					current_token = ""
		if current_token:
			tokens.append(current_token)
		return tokens

	tokenized_text = split_string_and_whitespace(text, 2)

	
	# Generate the bigrams
	bigrams = zip(tokenized_text, tokenized_text[1:])
	#print(f"Zipping \"tokenized_text\":\n\"\"\"\n{tokenized_text}\n\"\"\"\nto \"tokenized_text[1:]\":\n\"\"\"\n{tokenized_text[1:]}\n\"\"\"")
	
	# Create a dictionary to store the bigram model
	bigram_model = defaultdict(lambda: defaultdict(lambda: 0))
	
	# Count the frequency of each bigram
	for w1, w2 in bigrams:
		bigram_model[w1][w2] += 1
	
	# Calculate the probabilities for each bigram
	for w1 in bigram_model:
		total_count = float(sum(bigram_model[w1].values()))
		for w2 in bigram_model[w1]:
			bigram_model[w1][w2] /= total_count
	
	return bigram_model

def print_bigram_model(bigram_model):
	"""
	Print the bigram model in a readable format.
	
	Args:
		bigram_model (dict): The bigram model as a nested dictionary.
	"""
	for w1 in bigram_model:
		print(f"\"{w1}\":")
		for w2, prob in bigram_model[w1].items():
			print(f"\t\"{w2}\": {prob}")

def generate_text(bigram_model, prompt, num_words=100):
	"""
	Generate text from a bigram model and a prompt.
	
	Args:
		bigram_model (dict): The bigram model as a nested dictionary.
		prompt (str): The prompt text.
		num_words (int): The number of words to generate.
	
	Returns:
		str: The generated text.
	"""
	# Tokenize the prompt text
	tokenized_prompt = prompt.split()
	
	# Start with the last word of the prompt
	current_word = tokenized_prompt[-1]
	
	# Generate the output text
	output_text = [current_word]
	
	for _ in range(num_words):
		# Check if the current word is in the bigram model.
		if current_word in bigram_model:
			# Get the next word based on the current word and the bigram model.
			next_word = random.choices(
				list(
					bigram_model[current_word].keys()
				), 
				weights=list(
					bigram_model[current_word].values()
				)
			)[0]
		else:
			# If the word is not in the bigram model, choose the most common word in the bigram model as the next word.
			next_word = max(bigram_model, key=lambda x: sum(bigram_model[x].values()))
			print(f"[WARNING] \"current_word\", \"{current_word}\", not in \"bigram_model\"! Setting \"next_word\" to most common word in \"bigram_model\", \"{next_word}\".")
			
		# Add the next word to the output text.
		output_text.append(next_word)
		
		# Update the current word.
		current_word = next_word
	
	return ' '.join(output_text)


# Prompt the user to enter the filename of a text file under the "./training_data" directory, 
# for which to build the bigram model with.	 If the file does not exist or no input is given, 
# load the example file "./training_data/maned_wolf_description.txt".
print("\n============================================================")
filename = input("Enter the filename of a text (\".txt\") file located in \"./training_data\" to build the bigram model with (leave blank for example file): ")
if (filename != ""):
	filepath = os.path.join("./training_data", filename)
	if os.path.isfile(filepath):
		# If file found, load it.
		print(f"\"{filename}\" found. Loading...")
		with open(filepath, 'r') as file:
			training_text = file.read()
		print(f"\"{filepath}\" loaded.")
	else:
		# If file not found, load example file.
		print(f"[WARNING] \"{filename}\" not found. Loading example file...")
		with open("./training_data/maned_wolf_description.txt", "r") as file:
			training_text = file.read()
		print("\"./training_data/maned_wolf_description.txt\" loaded.")
else:
	# If no filename is entered, load example file.
	print("No filename entered. Loading example file...")
	with open("./training_data/maned_wolf_description.txt", "r") as file:
		training_text = file.read()
	print("\"./training_data/maned_wolf_description.txt\" loaded.")
print("\n============================================================")


# Build the bigram model. Before building, print a short 
# 25 word preview of the training text.
training_text_preview = ' '.join(islice(training_text.split(), 25))
print(f"Building bigram model from text:\n\"\"\"\n{training_text_preview}\n\"\"\"")
bigram_model = build_bigram_model(training_text)
print("\nFinished building bigram model.")
print("\n============================================================")

# Print the bigram model.
print("Bigram model (first word -> second word: probability):")
print_bigram_model(bigram_model)
print("\n============================================================")

# Prompt user for input word that will be used as the 
# generation prompt. If nothing is entered, quit.
while (True):
	prompt_text = input("Enter a generation prompt word. The prompt word must be in the built bigram model. Enter nothing to quit: ")
	if (prompt_text == ""):
		break;
	generated_text = generate_text(bigram_model, prompt_text)
	print(f"\nGenerated text from prompt \"{prompt_text}\":\n\"\"\"\n{generated_text}\n\"\"\"")
	print("\n============================================================")
print("Nothing entered, quitting.")
print("\n============================================================")