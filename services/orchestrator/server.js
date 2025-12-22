import express from "express";
import axios from "axios";
import cors from "cors";

const app = express();
app.use(express.json());
app.use(cors());

const PREPROCESS_URL = "http://preprocessor:5001/process";
const MODEL_SELECTOR_URL = "http://modelselector:5000/select";
const TRAINER_URL = "http://trainer:5002/train";
const EVALUATOR_URL = "http://evaluator:5003/evaluate";

app.post("/run-pipeline", async (req, res) => {
  try {
    const { datasetPath } = req.body;
    console.log("Pipeline started...");

    // 1️⃣ Preprocess
    console.log("Preprocessing...");
    const pre = await axios.post(PREPROCESS_URL, { datasetPath });
    const processedDataPath = pre.data.processedDataPath;

    // 2️⃣ Model Selection
    console.log("Selecting Model...");
    const model = await axios.post(MODEL_SELECTOR_URL, {
      datasetPath: processedDataPath
    });

    const selectedModel = model.data.modelName;
    console.log("Model Selected:", selectedModel);

    // 3️⃣ Training
    console.log("Training...");
    const train = await axios.post(TRAINER_URL, {
      datasetPath: processedDataPath,
      modelName: selectedModel
    });

    const trainedModelPath = train.data.modelPath;

    // 4️⃣ Evaluation
    console.log("Evaluating...");
    const evalRes = await axios.post(EVALUATOR_URL, {
      modelPath: trainedModelPath,
      datasetPath: processedDataPath
    });

    console.log("Pipeline Completed!");

    return res.json({
      status: "SUCCESS",
      model: selectedModel,
      trainedModelPath,
      evaluation: evalRes.data
    });

  } catch (err) {
    console.error(err.message);
    return res.status(500).json({
      status: "FAILED",
      error: err.message
    });
  }
});

app.listen(5004, () => console.log("Orchestrator running on 5004 🚀"));
