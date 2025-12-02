import { BookOpen } from "lucide-react";
import Link from "next/link";

import { Button } from "@/components/ui/button";

type ExamProps = {
    id: number;
    title: string;
    description: string;
    lessonsCount: number;
    questionsCount: number;
};

export const Exam = ({
    id,
    title,
    description,
    lessonsCount,
    questionsCount,
}: ExamProps) => {
    return (
        <div className="rounded-xl border-2 border-neutral-200 p-6 bg-white hover:shadow-md transition">
            <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-x-3">
                    <div className="rounded-lg bg-green-500 p-3">
                        <BookOpen className="h-6 w-6 text-white" />
                    </div>
                    <div>
                        <h3 className="font-bold text-lg text-neutral-700">
                            {title}
                        </h3>
                        <p className="text-sm text-neutral-500">
                            {description}
                        </p>
                    </div>
                </div>
            </div>

            <div className="flex items-center justify-between text-sm text-neutral-600 mb-4">
                <span>{lessonsCount} lecciones</span>
                <span>{questionsCount} preguntas</span>
            </div>

            <Link href={`/exam/${id}`}>
                <Button className="w-full" variant="primary" size="lg">
                    Iniciar Examen
                </Button>
            </Link>
        </div>
    );
};
