"use client";

import { useState, useTransition } from "react";

import { useAudio } from "react-use";

import { challengeOptions, challenges, userSubscription } from "@/db/schema";

import { Challenge } from "./challenge";
import { Footer } from "./footer";
import { Header } from "./header";
import { QuestionBubble } from "./question-bubble";
import { ResultsScreen } from "./results-screen";

type Challenge = typeof challenges.$inferSelect & {
    challengeOptions: (typeof challengeOptions.$inferSelect)[];
};

type Result = {
    challenge: Challenge;
    userOptionId?: number;
    status: "correct" | "wrong";
};

type ExamQuizProps = {
    initialLessonId: number;
    initialLessonChallenges: (typeof challenges.$inferSelect & {
        completed: boolean;
        challengeOptions: (typeof challengeOptions.$inferSelect)[];
    })[];
    userSubscription:
    | (typeof userSubscription.$inferSelect & {
        isActive: boolean;
    })
    | null;
};

export const ExamQuiz = ({
    initialLessonChallenges,
    userSubscription,
}: ExamQuizProps) => {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const [correctAudio, _c, correctControls] = useAudio({ src: "/correct.wav" });
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const [incorrectAudio, _i, incorrectControls] = useAudio({
        src: "/incorrect.wav",
    });

    const [pending, startTransition] = useTransition();


    const [percentage, setPercentage] = useState(0);
    const [challenges] = useState(initialLessonChallenges);
    const [activeIndex, setActiveIndex] = useState(0);

    const [selectedOption, setSelectedOption] = useState<number>();
    const [status, setStatus] = useState<"none" | "wrong" | "correct">("none");

    const [results, setResults] = useState<Result[]>([]);

    const challenge = challenges[activeIndex];
    const options = challenge?.challengeOptions ?? [];

    const onNext = () => {
        setActiveIndex((current) => current + 1);
    };

    const onSelect = (id: number) => {
        if (status !== "none") return;

        setSelectedOption(id);
    };

    const onContinue = () => {
        if (!selectedOption) return;

        if (status === "wrong" || status === "correct") {
            onNext();
            setStatus("none");
            setSelectedOption(undefined);
            return;
        }

        const correctOption = options.find((option) => option.correct);

        if (!correctOption) return;

        if (correctOption.id === selectedOption) {
            startTransition(() => {
                void correctControls.play();
                setStatus("correct");
                setPercentage((prev) => prev + 100 / challenges.length);

                setResults((prev) => [
                    ...prev,
                    { challenge, userOptionId: selectedOption, status: "correct" },
                ]);
            });
        } else {
            startTransition(() => {
                void incorrectControls.play();
                setStatus("wrong");

                setResults((prev) => [
                    ...prev,
                    { challenge, userOptionId: selectedOption, status: "wrong" },
                ]);
            });
        }
    };

    if (!challenge) {
        return <ResultsScreen results={results} />;
    }

    const title =
        challenge.type === "ASSIST"
            ? "Selecciona el significado correcto"
            : challenge.question;

    return (
        <>
            {incorrectAudio}
            {correctAudio}
            <Header
                hearts={Infinity}
                percentage={percentage}
                hasActiveSubscription={!!userSubscription?.isActive}
            />

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
                                status={status}
                                selectedOption={selectedOption}
                                disabled={pending}
                                type={challenge.type}
                                audioSrc={challenge.audioSrc}
                            />
                        </div>
                    </div>
                </div>
            </div>

            <Footer
                disabled={pending || !selectedOption}
                status={status}
                onCheck={onContinue}
            />
        </>
    );
};
