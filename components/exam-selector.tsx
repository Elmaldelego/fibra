"use client";

import { ChevronDown } from "lucide-react";

import { Button } from "@/components/ui/button";
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

type Exam = {
    id: number;
    title: string;
    description: string;
    order: number;
};

type Props = {
    exams: Exam[];
    selectedExamId: number | null;
    onSelectExam: (examId: number | null) => void;
};

export const ExamSelector = ({ exams, selectedExamId, onSelectExam }: Props) => {
    const selectedExam = exams.find((e) => e.id === selectedExamId);

    return (
        <DropdownMenu>
            <DropdownMenuTrigger asChild>
                <Button variant="ghost" className="w-full justify-between" size="lg">
                    <div className="flex items-center gap-x-2">
                        <span className="font-bold text-neutral-700">
                            {selectedExam ? selectedExam.title : "Todos los exámenes"}
                        </span>
                    </div>
                    <ChevronDown className="h-4 w-4 text-neutral-500 opacity-50" />
                </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-[250px]">
                <DropdownMenuItem
                    onClick={() => onSelectExam(null)}
                    className="cursor-pointer"
                >
                    <div className="flex items-center gap-x-2 w-full">
                        <span className="font-bold text-neutral-700">
                            Todos los exámenes
                        </span>
                    </div>
                </DropdownMenuItem>
                {exams.map((exam) => (
                    <DropdownMenuItem
                        key={exam.id}
                        onClick={() => onSelectExam(exam.id)}
                        className="cursor-pointer"
                    >
                        <div className="flex flex-col gap-y-1 w-full">
                            <span className="font-bold text-neutral-700">
                                {exam.title}
                            </span>
                            <span className="text-xs text-neutral-500">
                                {exam.description}
                            </span>
                        </div>
                    </DropdownMenuItem>
                ))}
            </DropdownMenuContent>
        </DropdownMenu>
    );
};
