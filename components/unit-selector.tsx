"use client";



import { ChevronDown } from "lucide-react";

import { Button } from "@/components/ui/button";
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

type Unit = {
    id: number;
    title: string;
    description: string;
    order: number;
};

type Props = {
    units: Unit[];
    selectedUnitId: number | null;
    onSelectUnit: (unitId: number | null) => void;
};

export const UnitSelector = ({ units, selectedUnitId, onSelectUnit }: Props) => {
    const selectedUnit = units.find((u) => u.id === selectedUnitId);

    return (
        <DropdownMenu>
            <DropdownMenuTrigger asChild>
                <Button variant="ghost" className="w-full justify-between" size="lg">
                    <div className="flex items-center gap-x-2">
                        <span className="font-bold text-neutral-700">
                            {selectedUnit ? selectedUnit.title : "Todas las unidades"}
                        </span>
                    </div>
                    <ChevronDown className="h-4 w-4 text-neutral-500 opacity-50" />
                </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-[250px]">
                <DropdownMenuItem
                    onClick={() => onSelectUnit(null)}
                    className="cursor-pointer"
                >
                    <div className="flex items-center gap-x-2 w-full">
                        <span className="font-bold text-neutral-700">
                            Todas las unidades
                        </span>
                    </div>
                </DropdownMenuItem>
                {units.map((unit) => (
                    <DropdownMenuItem
                        key={unit.id}
                        onClick={() => onSelectUnit(unit.id)}
                        className="cursor-pointer"
                    >
                        <div className="flex flex-col gap-y-1 w-full">
                            <span className="font-bold text-neutral-700">
                                {unit.title}
                            </span>
                            <span className="text-xs text-neutral-500">
                                {unit.description}
                            </span>
                        </div>
                    </DropdownMenuItem>
                ))}
            </DropdownMenuContent>
        </DropdownMenu>
    );
};
