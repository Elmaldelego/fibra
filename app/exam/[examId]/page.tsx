import { redirect } from "next/navigation";

import { ExamQuiz } from "@/app/exam/exam-quiz";
import { getExamById, getUserProgress } from "@/db/queries";

type ExamPageProps = {
    params: {
        examId: number;
    };
};

const ExamPage = async ({ params }: ExamPageProps) => {
    const examData = getExamById(params.examId);
    const userProgressData = getUserProgress();

    const [exam, userProgress] = await Promise.all([
        examData,
        userProgressData,
    ]);

    if (!exam || !userProgress) return redirect("/simulator");

    // Flatten all challenges from all lessons in the exam
    const allChallenges = exam.examLessons.flatMap((examLesson) =>
        examLesson.lesson.challenges.map((challenge) => ({
            ...challenge,
            lessonTitle: examLesson.lesson.title,
        }))
    );

    return (
        <ExamQuiz
            examId={exam.id}
            examTitle={exam.title}
            challenges={allChallenges}
        />
    );
};

export default ExamPage;
