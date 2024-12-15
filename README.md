# ArmTTS API Example

This repository demonstrates a simple Python server for interacting with the ArmTTS API. It allows you to send text and receive audio responses using HTTP requests.

## Getting Started

### Prerequisites
1. Python 3.x installed on your machine.
2. An API subscription to ArmTTS on [RapidAPI]([https://rapidapi.com/](https://rapidapi.com/albertgrigoryan/api/armtts1)).

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/armtts-api-example.git
   cd armtts-api-example
   ```
2. Install dependencies:
   ```bash
   pip3 install -r requires.txt
   ```

3. Set your `RapidAPI_KEY` in the `server.py` file:

### Running the Server
Start the Flash server:
```bash
python3 server.py
```
The server will run locally at `http://localhost:5001`.

## Request Example

You can use `curl` to test the API. Replace the text in the example below with your desired input:

```bash
curl --location 'http://localhost:5001/play' \
--form 'text="Ողջույն, իմ անունը Գոռ է։"'
```

The server will return a response containing the synthesized audio.

## Postman Collection

For convenience, an exported Postman collection is included in the `docs` folder:

- **Path:** `docs/ArmTTS Web API.postman_collection.json`

Import this file into Postman to explore the API with a user-friendly interface.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
