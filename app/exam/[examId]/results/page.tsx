import { CheckCircle2, XCircle } from "lucide-react";
import Link from "next/link";
import { redirect } from "next/navigation";

import { Button } from "@/components/ui/button";
import { getExamById, getExamResults } from "@/db/queries";

type ResultsPageProps = {
    params: {
        examId: number;
    };
    searchParams: {
        score?: string;
        total?: string;
    };
};

const ResultsPage = async ({ params, searchParams }: ResultsPageProps) => {
    const examData = getExamById(params.examId);
    const resultsData = getExamResults(params.examId);

    const [exam, results] = await Promise.all([examData, resultsData]);

    if (!exam) return redirect("/simulator");

    const latestResult = results[0];
    const score = searchParams.score ? parseInt(searchParams.score) : latestResult?.score || 0;
    const total = searchParams.total ? parseInt(searchParams.total) : latestResult?.totalQuestions || 0;
    const percentage = total > 0 ? Math.round((score / total) * 100) : 0;

    // Get all challenges with their correct answers
    const allChallenges = exam.examLessons.flatMap((examLesson) =>
        examLesson.lesson.challenges.map((challenge) => ({
            ...challenge,
            lessonTitle: examLesson.lesson.title,
        }))
    );

    const userAnswers = latestResult?.answers || [];

    return (
        <div className="flex flex-col h-screen">
            {/* Header */}
            <div className="border-b-2 px-6 py-4">
                <h1 className="text-2xl font-bold text-neutral-700">
                    Resultados del Examen: {exam.title}
                </h1>
            </div>

            {/* Score Summary */}
            <div className="bg-gradient-to-r from-green-50 to-blue-50 px-6 py-8">
                <div className="max-w-4xl mx-auto">
                    <div className="bg-white rounded-xl shadow-lg p-8">
                        <div className="text-center">
                            <h2 className="text-4xl font-bold text-neutral-800 mb-2">
                                {percentage}%
                            </h2>
                            <p className="text-lg text-neutral-600 mb-4">
                                {score} de {total} respuestas correctas
                            </p>
                            <div className="flex items-center justify-center gap-x-4 text-sm">
                                <div className="flex items-center gap-x-2 text-green-600">
                                    <CheckCircle2 className="h-5 w-5" />
                                    <span>{score} correctas</span>
                                </div>
                                <div className="flex items-center gap-x-2 text-red-600">
                                    <XCircle className="h-5 w-5" />
                                    <span>{total - score} incorrectas</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Detailed Results */}
            <div className="flex-1 overflow-y-auto px-6 py-8">
                <div className="max-w-4xl mx-auto">
                    <h3 className="text-xl font-bold text-neutral-700 mb-6">
                        Revisión de Respuestas
                    </h3>

                    <div className="space-y-6">
                        {allChallenges.map((challenge, index) => {
                            const userAnswer = userAnswers.find(
                                (a) => a.challengeId === challenge.id
                            );
                            const correctOption = challenge.challengeOptions.find(
                                (opt) => opt.correct
                            );
                            const selectedOption = challenge.challengeOptions.find(
                                (opt) => opt.id === userAnswer?.selectedOptionId
                            );
                            const isCorrect = userAnswer?.correct ?? false;

                            return (
                                <div
                                    key={challenge.id}
                                    className={`rounded-lg border-2 p-6 ${isCorrect
                                        ? "border-green-200 bg-green-50"
                                        : "border-red-200 bg-red-50"
                                        }`}
                                >
                                    <div className="flex items-start justify-between mb-4">
                                        <div className="flex-1">
                                            <div className="flex items-center gap-x-2 mb-2">
                                                {isCorrect ? (
                                                    <CheckCircle2 className="h-5 w-5 text-green-600" />
                                                ) : (
                                                    <XCircle className="h-5 w-5 text-red-600" />
                                                )}
                                                <span className="text-sm font-semibold text-neutral-600">
                                                    Pregunta {index + 1} - {challenge.lessonTitle}
                                                </span>
                                            </div>
                                            <h4 className="text-lg font-bold text-neutral-800">
                                                {challenge.question}
                                            </h4>
                                        </div>
                                    </div>

                                    <div className="space-y-2">
                                        {!isCorrect && selectedOption && (
                                            <div className="bg-red-100 border border-red-300 rounded-lg p-3">
                                                <p className="text-sm font-semibold text-red-800 mb-1">
                                                    Tu respuesta:
                                                </p>
                                                <p className="text-red-700">{selectedOption.text}</p>
                                            </div>
                                        )}

                                        <div className="bg-green-100 border border-green-300 rounded-lg p-3">
                                            <p className="text-sm font-semibold text-green-800 mb-1">
                                                Respuesta correcta:
                                            </p>
                                            <p className="text-green-700">{correctOption?.text}</p>
                                        </div>
                                    </div>
                                </div>
                            );
                        })}
                    </div>
                </div>
            </div>

            {/* Actions */}
            <div className="border-t-2 px-6 py-4">
                <div className="max-w-4xl mx-auto flex gap-x-4">
                    <Link href="/simulator" className="flex-1">
                        <Button variant="secondary" className="w-full" size="lg">
                            Volver al Simulador
                        </Button>
                    </Link>
                    <Link href={`/exam/${params.examId}`} className="flex-1">
                        <Button variant="primary" className="w-full" size="lg">
                            Reintentar Examen
                        </Button>
                    </Link>
                </div>
            </div>
        </div>
    );
};

export default ResultsPage;
