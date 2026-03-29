import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ArrowRight, ArrowLeft } from "lucide-react";
import { Button } from "@/components/ui/button";

interface WizardFlowProps {
  onComplete: (data: { activity: string; income: string }) => void;
}

const incomeOptions = [
  "Até R$ 6.750",
  "Entre R$ 6.750 e R$ 30.000",
  "Acima de R$ 30.000",
  "Ainda não tenho renda fixa",
];

const WizardFlow = ({ onComplete }: WizardFlowProps) => {
  const [step, setStep] = useState(0);
  const [activity, setActivity] = useState("");
  const [income, setIncome] = useState("");

  const handleNext = () => {
    if (step === 0 && activity.trim()) {
      setStep(1);
    }
  };

  const handleSelectIncome = (option: string) => {
    setIncome(option);
    setTimeout(() => {
      onComplete({ activity, income: option });
    }, 400);
  };

  const slideVariants = {
    enter: { opacity: 0, x: 60 },
    center: { opacity: 1, x: 0 },
    exit: { opacity: 0, x: -60 },
  };

  return (
    <div className="flex min-h-screen flex-col items-center justify-center px-6">
      <div className="w-full max-w-lg">
        {/* Progress */}
        <div className="mb-10 flex gap-2">
          {[0, 1].map((i) => (
            <div
              key={i}
              className={`h-1.5 flex-1 rounded-full transition-colors duration-300 ${
                i <= step ? "bg-primary" : "bg-border"
              }`}
            />
          ))}
        </div>

        <AnimatePresence mode="wait">
          {step === 0 && (
            <motion.div
              key="step0"
              variants={slideVariants}
              initial="enter"
              animate="center"
              exit="exit"
              transition={{ duration: 0.35 }}
            >
              <p className="mb-2 text-sm font-medium text-muted-foreground">
                Passo 1 de 2
              </p>
              <h2 className="mb-6 text-2xl font-bold text-foreground md:text-3xl">
                Me conte com as suas palavras: o que você faz no dia a dia para
                gerar renda?
              </h2>
              <textarea
                value={activity}
                onChange={(e) => setActivity(e.target.value)}
                placeholder="Ex: Faço bolos por encomenda, vendo roupas online, trabalho como eletricista..."
                className="mb-6 h-36 w-full resize-none rounded-xl border-2 border-border bg-card p-4 text-foreground placeholder:text-muted-foreground/60 focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20 transition-all"
              />
              <Button
                variant="hero"
                size="lg"
                onClick={handleNext}
                disabled={!activity.trim()}
                className="w-full sm:w-auto"
              >
                Avançar
                <ArrowRight className="ml-1 h-4 w-4" />
              </Button>
            </motion.div>
          )}

          {step === 1 && (
            <motion.div
              key="step1"
              variants={slideVariants}
              initial="enter"
              animate="center"
              exit="exit"
              transition={{ duration: 0.35 }}
            >
              <button
                onClick={() => setStep(0)}
                className="mb-4 flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground transition-colors"
              >
                <ArrowLeft className="h-4 w-4" /> Voltar
              </button>
              <p className="mb-2 text-sm font-medium text-muted-foreground">
                Passo 2 de 2
              </p>
              <h2 className="mb-8 text-2xl font-bold text-foreground md:text-3xl">
                Mais ou menos, quanto você ganha por mês com isso?
              </h2>
              <div className="flex flex-col gap-3">
                {incomeOptions.map((option) => (
                  <Button
                    key={option}
                    variant={income === option ? "choiceSelected" : "choice"}
                    size="lg"
                    className="justify-start text-left"
                    onClick={() => handleSelectIncome(option)}
                  >
                    {option}
                  </Button>
                ))}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};

export default WizardFlow;
