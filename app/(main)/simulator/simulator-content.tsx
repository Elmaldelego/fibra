"use client";

import { useState } from "react";

import { ExamSelector } from "@/components/exam-selector";
import { FeedWrapper } from "@/components/feed-wrapper";

import { Exam } from "./exam";
import { Header } from "../learn/header";

type ExamLesson = {
    id: number;
    examId: number;
    lessonId: number;
    order: number;
    lesson: {
        id: number;
        title: string;
        unitId: number;
        order: number;
        challenges: {
            id: number;
            lessonId: number;
            type: "SELECT" | "ASSIST" | "LISTEN";
            question: string;
            order: number;
        }[];
    };
};

type ExamType = {
    id: number;
    title: string;
    description: string;
    courseId: number;
    order: number;
    examLessons: ExamLesson[];
};

type Props = {
    exams: ExamType[];
};

export const SimulatorContent = ({ exams }: Props) => {
    const [selectedExamId, setSelectedExamId] = useState<number | null>(null);

    // Filter exams based on selection
    const displayedExams = selectedExamId
        ? exams.filter((exam) => exam.id === selectedExamId)
        : exams;

    return (
        <FeedWrapper>
            <Header title="Simulador">
                <ExamSelector
                    exams={exams.map((e) => ({
                        id: e.id,
                        title: e.title,
                        description: e.description,
                        order: e.order,
                    }))}
                    selectedExamId={selectedExamId}
                    onSelectExam={setSelectedExamId}
                />
            </Header>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-6">
                {displayedExams.map((exam) => {
                    const questionsCount = exam.examLessons.reduce(
                        (total, examLesson) => total + examLesson.lesson.challenges.length,
                        0
                    );

                    return (
                        <Exam
                            key={exam.id}
                            id={exam.id}
                            title={exam.title}
                            description={exam.description}
                            lessonsCount={exam.examLessons.length}
                            questionsCount={questionsCount}
                        />
                    );
                })}
            </div>
        </FeedWrapper>
    );
};
