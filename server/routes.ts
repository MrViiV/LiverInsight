import type { Express } from "express";
import { createServer, type Server } from "http";
import { z } from "zod";
import { insertPredictionSchema } from "@shared/schema";
import { storage } from "./storage";

export async function registerRoutes(app: Express): Promise<Server> {
  // Liver disease prediction endpoint
  app.post("/api/predict", async (req, res) => {
    try {
      // Validate request body
      const validationResult = insertPredictionSchema.safeParse(req.body);
      if (!validationResult.success) {
        return res.status(400).json({
          message: "Invalid input data",
          errors: validationResult.error.errors,
        });
      }

      const data = validationResult.data;

      // Calculate risk score using prediction algorithm
      const result = await storage.predictLiverDisease(data);

      res.json(result);
    } catch (error: any) {
      console.error("Prediction error:", error);
      
      // Check if it's an ML service specific error
      if (error.message?.includes('ML prediction service unavailable')) {
        return res.status(503).json({
          message: "ML prediction service unavailable",
          details: "The machine learning service is not running. Please ensure both model and scaler files are available and the ML service is started.",
          error: error.message
        });
      }
      
      res.status(500).json({
        message: "Internal server error during prediction",
        error: error.message || "Unknown error occurred"
      });
    }
  });

  // Get prediction history (optional)
  app.get("/api/predictions", async (req, res) => {
    try {
      const predictions = await storage.getAllPredictions();
      res.json(predictions);
    } catch (error) {
      console.error("Error fetching predictions:", error);
      res.status(500).json({
        message: "Failed to fetch prediction history",
      });
    }
  });

  const httpServer = createServer(app);
  return httpServer;
}
