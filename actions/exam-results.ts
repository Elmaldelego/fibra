"use server";

import { auth } from "@clerk/nextjs/server";
import db from "@/db/drizzle";
import { examResults } from "@/db/schema";

export const saveExamResultAction = async (
    examId: number,
    score: number,
    totalQuestions: number,
    answers: { challengeId: number; selectedOptionId: number; correct: boolean }[]
) => {
    const { userId } = await auth();

    if (!userId) {
        return { error: "Unauthorized" };
    }

    try {
        await db.insert(examResults).values({
            userId,
            examId,
            score,
            totalQuestions,
            answers: JSON.stringify(answers),
        });

        return { success: true };
    } catch (error) {
        console.error("Error saving exam result:", error);
        return { error: "Failed to save exam result" };
    }
};
