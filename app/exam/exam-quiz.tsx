"use client";

import { useState } from "react";

import { useRouter } from "next/navigation";
import { toast } from "sonner";

import { saveExamResultAction } from "@/actions/exam-results";
import { challengeOptions, challenges } from "@/db/schema";

import { Challenge } from "../lesson/challenge";
import { Footer } from "../lesson/footer";
import { QuestionBubble } from "../lesson/question-bubble";

type ExamQuizProps = {
    examId: number;
    examTitle: string;
    challenges: (typeof challenges.$inferSelect & {
        lessonTitle: string;
        challengeOptions: (typeof challengeOptions.$inferSelect)[];
    })[];
};

export const ExamQuiz = ({
    examId,
    examTitle,
    challenges,
}: ExamQuizProps) => {
    const router = useRouter();
    const [activeIndex, setActiveIndex] = useState(0);
    const [selectedOption, setSelectedOption] = useState<number>();
    const [answers, setAnswers] = useState<
        { challengeId: number; selectedOptionId: number; correct: boolean }[]
    >([]);

    const challenge = challenges[activeIndex];
    const options = challenge?.challengeOptions ?? [];
    const percentage = ((activeIndex + 1) / challenges.length) * 100;

    const onSelect = (id: number) => {
        setSelectedOption(id);
    };

    const onContinue = () => {
        if (!selectedOption) return;

        const correctOption = options.find((option) => option.correct);
        if (!correctOption) return;

        const isCorrect = correctOption.id === selectedOption;

        // Save answer
        setAnswers((prev) => [
            ...prev,
            {
                challengeId: challenge.id,
                selectedOptionId: selectedOption,
                correct: isCorrect,
            },
        ]);

        // Move to next question
        if (activeIndex < challenges.length - 1) {
            setActiveIndex((current) => current + 1);
            setSelectedOption(undefined);
        } else {
            // Exam finished - save results
            const finalAnswers = [
                ...answers,
                {
                    challengeId: challenge.id,
                    selectedOptionId: selectedOption,
                    correct: isCorrect,
                },
            ];

            const score = finalAnswers.filter((a) => a.correct).length;

            void (async () => {
                try {
                    const result = await saveExamResultAction(examId, score, challenges.length, finalAnswers);

                    if (result.error) {
                        toast.error("Error al guardar resultados");
                        return;
                    }

                    router.push(`/exam/${examId}/results?score=${score}&total=${challenges.length}`);
                } catch (error) {
                    toast.error("Error al guardar resultados");
                    console.error(error);
                }
            })();
        }
    };
    if (!challenge) {
        return null;
    }

    const title =
        challenge.type === "ASSIST"
            ? "Selecciona el significado correcto"
            : challenge.question;

    return (
        <>
            <div className="flex flex-col h-screen">
                {/* Header */}
                <div className="flex items-center justify-between px-6 py-4 border-b-2">
                    <h2 className="text-lg font-bold text-neutral-700">{examTitle}</h2>
                    <div className="flex items-center gap-x-4">
                        <span className="text-sm text-neutral-500">
                            Pregunta {activeIndex + 1} de {challenges.length}
                        </span>
                        <div className="w-32 h-3 bg-neutral-200 rounded-full">
                            <div
                                className="h-full bg-green-500 rounded-full transition-all"
                                style={{ width: `${percentage}%` }}
                            />
                        </div>
                    </div>
                </div>

                {/* Content */}
                <div className="flex-1">
                    <div className="flex h-full items-center justify-center">
                        <div className="flex w-full flex-col gap-y-12 px-6 lg:min-h-[350px] lg:w-[600px] lg:px-0">
                            <h1 className="text-center text-lg font-bold text-neutral-700 lg:text-start lg:text-3xl">
                                {title}
                            </h1>

                            <div>
                                {challenge.type === "ASSIST" && (
                                    <QuestionBubble question={challenge.question} />
                                )}

                                <Challenge
                                    options={options}
                                    onSelect={onSelect}
                                    status="none"
                                    selectedOption={selectedOption}
                                    disabled={false}
                                    type={challenge.type}
                                    audioSrc={challenge.audioSrc}
                                />
                            </div>
                        </div>
                    </div>
                </div>

                {/* Footer */}
                <Footer
                    disabled={!selectedOption}
                    status="none"
                    onCheck={onContinue}
                />
            </div>
        </>
    );
};
