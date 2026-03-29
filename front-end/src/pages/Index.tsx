import { useState } from "react";
import LandingScreen from "@/components/LandingScreen";
import WizardFlow from "@/components/WizardFlow";
import LoadingScreen from "@/components/LoadingScreen";
import ResultDashboard from "@/components/ResultDashboard";

type Screen = "landing" | "wizard" | "loading" | "result";

const Index = () => {
  const [screen, setScreen] = useState<Screen>("landing");
  const [category, setCategory] = useState("MEI");

  const handleStart = () => setScreen("wizard");

  const handleWizardComplete = (data: { activity: string; income: string }) => {
    setScreen("loading");

    // Simulate AI analysis
    setTimeout(() => {
      const isME =
        data.income === "Entre R$ 6.750 e R$ 30.000" ||
        data.income === "Acima de R$ 30.000";
      setCategory(isME ? "ME" : "MEI");
      setScreen("result");
    }, 3000);
  };

  const handleRestart = () => {
    setScreen("landing");
    setCategory("MEI");
  };

  return (
    <>
      {screen === "landing" && <LandingScreen onStart={handleStart} />}
      {screen === "wizard" && <WizardFlow onComplete={handleWizardComplete} />}
      {screen === "loading" && <LoadingScreen />}
      {screen === "result" && (
        <ResultDashboard category={category} onRestart={handleRestart} />
      )}
    </>
  );
};

export default Index;
