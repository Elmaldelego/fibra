import { redirect } from "next/navigation";

import { ExamQuiz } from "@/app/lesson/exam-quiz";
import { getLesson, getUserProgress, getUserSubscription } from "@/db/queries";

type Props = {
    params: {
        lessonId: string;
    };
};

const ExamPage = async ({ params }: Props) => {
    const lessonData = getLesson(Number(params.lessonId));
    const userProgressData = getUserProgress();
    const userSubscriptionData = getUserSubscription();

    const [lesson, userProgress, userSubscription] = await Promise.all([
        lessonData,
        userProgressData,
        userSubscriptionData,
    ]);

    if (!lesson || !userProgress) return redirect("/learn");

    return (
        <ExamQuiz
            initialLessonId={lesson.id}
            initialLessonChallenges={lesson.challenges}
            userSubscription={userSubscription}
        />
    );
};

export default ExamPage;
