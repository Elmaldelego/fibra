"use client";

import Image from "next/image";
import { useRouter } from "next/navigation";

import { Button } from "@/components/ui/button";
import { challengeOptions, challenges } from "@/db/schema";
import { cn } from "@/lib/utils";

type Challenge = typeof challenges.$inferSelect & {
    challengeOptions: (typeof challengeOptions.$inferSelect)[];
};

type Result = {
    challenge: Challenge;
    userOptionId?: number;
    status: "correct" | "wrong";
};

type ResultsScreenProps = {
    results: Result[];
};

export const ResultsScreen = ({ results }: ResultsScreenProps) => {
    const router = useRouter();
    const correctCount = results.filter((r) => r.status === "correct").length;
    const incorrectCount = results.length - correctCount;

    return (
        <div className="flex flex-col items-center justify-center gap-y-4 p-6 lg:gap-y-8">
            <div className="flex flex-col items-center gap-y-2">
                <Image src="/finish.svg" alt="Finish" height={100} width={100} />
                <h1 className="text-xl font-bold text-neutral-700 lg:text-3xl">
                    Resultados del Examen
                </h1>
                <p className="text-lg text-neutral-500">
                    Obtuviste <span className="font-bold text-green-500">{correctCount}</span>{" "}
                    correctas e{" "}
                    <span className="font-bold text-rose-500">{incorrectCount}</span>{" "}
                    incorrectas.
                </p>
            </div>

            <div className="w-full max-w-2xl space-y-4">
                {results.map((result, index) => {
                    const { challenge, userOptionId, status } = result;
                    const correctOption = challenge.challengeOptions.find((o) => o.correct);
                    const userOption = challenge.challengeOptions.find(
                        (o) => o.id === userOptionId
                    );

                    return (
                        <div
                            key={challenge.id}
                            className={cn(
                                "rounded-xl border-2 p-4",
                                status === "correct"
                                    ? "border-green-500 bg-green-50"
                                    : "border-rose-500 bg-rose-50"
                            )}
                        >
                            <div className="mb-2 flex items-center justify-between">
                                <h3 className="font-bold text-neutral-700">
                                    Pregunta {index + 1}
                                </h3>
                                <span
                                    className={cn(
                                        "text-sm font-bold uppercase",
                                        status === "correct" ? "text-green-500" : "text-rose-500"
                                    )}
                                >
                                    {status === "correct" ? "Correcto" : "Incorrecto"}
                                </span>
                            </div>
                            <p className="mb-4 text-neutral-600">{challenge.question}</p>

                            <div className="space-y-2">
                                <div className="flex items-center gap-x-2">
                                    <span className="text-sm font-bold text-neutral-500">
                                        Tu Respuesta:
                                    </span>
                                    <span
                                        className={cn(
                                            "text-sm font-bold",
                                            status === "correct" ? "text-green-600" : "text-rose-600"
                                        )}
                                    >
                                        {userOption?.text || "Sin respuesta"}
                                    </span>
                                </div>
                                {status === "wrong" && (
                                    <div className="flex items-center gap-x-2">
                                        <span className="text-sm font-bold text-neutral-500">
                                            Respuesta Correcta:
                                        </span>
                                        <span className="text-sm font-bold text-green-600">
                                            {correctOption?.text}
                                        </span>
                                    </div>
                                )}
                            </div>
                        </div>
                    );
                })}
            </div>

            <Button
                variant="primary"
                className="w-full max-w-xs"
                onClick={() => router.push("/simulator")}
            >
                Volver al Simulador
            </Button>
        </div>
    );
};
