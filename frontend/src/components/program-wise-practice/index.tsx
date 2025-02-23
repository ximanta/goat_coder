"use client"

import React, { useState } from 'react';
import { ChevronRight, FolderOpen, BookOpen, Zap } from 'lucide-react';
import programData from '@/data/program_data.json';

interface Sprint {
  sprintId: string;
  sprintName: string;
  sprintDescription: string;
  concept: string;
  learningObjectives: string[];
  isPlatformEnabled: boolean;
}

interface Course {
  courseId: string;
  courseName: string;
  concept: string;
  sprints: Sprint[];
  isPlatformEnabled: boolean;
}

interface Program {
  programId: string;
  programName: string;
  courses: Course[];
}

const ProgramWisePractice = ({ onSprintSelect }: { onSprintSelect: (concept: string) => void }) => {
  const [selectedProgram, setSelectedProgram] = useState<Program | null>(null);
  const [selectedCourse, setSelectedCourse] = useState<Course | null>(null);

  const getEnabledCourses = (program: Program) => {
    return program.courses.filter(course => course.isPlatformEnabled);
  };

  const getEnabledSprints = (course: Course) => {
    return course.sprints.filter(sprint => sprint.isPlatformEnabled);
  };

  const handleProgramClick = (program: Program) => {
    setSelectedProgram(program);
    setSelectedCourse(null);
  };

  const handleCourseClick = (course: Course) => {
    setSelectedCourse(course);
  };

  const handleSprintClick = (sprint: Sprint) => {
    onSprintSelect(sprint.concept);
  };

  const handleBack = () => {
    if (selectedCourse) {
      setSelectedCourse(null);
    } else if (selectedProgram) {
      setSelectedProgram(null);
    }
  };

  // Filter out programs that have no enabled courses
  const availablePrograms = programData.programs.filter(program => 
    getEnabledCourses(program).length > 0
  );

  return (
    <div className="mb-12">
      <h3 className="text-2xl font-bold text-gray-900 mb-8">Program Wise Practice</h3>
      
      {/* Navigation */}
      {(selectedProgram || selectedCourse) && (
        <button
          onClick={handleBack}
          className="mb-4 text-indigo-600 hover:text-indigo-800 flex items-center"
        >
          ← Back
        </button>
      )}

      {/* Programs List */}
      {!selectedProgram && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {availablePrograms.map((program) => {
            const enabledCourses = getEnabledCourses(program);
            return (
              <button
                key={program.programId}
                onClick={() => handleProgramClick(program)}
                className="bg-white p-6 rounded-lg shadow-sm hover:shadow-md transition-shadow text-left"
              >
                <div className="flex items-center gap-4 mb-4">
                  <FolderOpen className="w-6 h-6 text-indigo-600" />
                  <h4 className="text-lg font-semibold">{program.programName}</h4>
                </div>
                <p className="text-gray-600">{enabledCourses.length} Courses</p>
              </button>
            );
          })}
        </div>
      )}

      {/* Courses List */}
      {selectedProgram && !selectedCourse && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {getEnabledCourses(selectedProgram).map((course) => {
            const enabledSprints = getEnabledSprints(course);
            return (
              <button
                key={course.courseId}
                onClick={() => handleCourseClick(course)}
                className="bg-white p-6 rounded-lg shadow-sm hover:shadow-md transition-shadow text-left"
              >
                <div className="flex items-center gap-4 mb-4">
                  <BookOpen className="w-6 h-6 text-indigo-600" />
                  <h4 className="text-lg font-semibold">{course.courseName}</h4>
                </div>
                <p className="text-gray-600">{enabledSprints.length} Sprints</p>
              </button>
            );
          })}
        </div>
      )}

      {/* Sprints List */}
      {selectedCourse && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {getEnabledSprints(selectedCourse).map((sprint) => (
            <button
              key={sprint.sprintId}
              onClick={() => handleSprintClick(sprint)}
              className="bg-white p-6 rounded-lg shadow-sm hover:shadow-md transition-shadow text-left"
            >
              <div className="flex items-center gap-4 mb-4">
                <Zap className="w-6 h-6 text-indigo-600" />
                <h4 className="text-lg font-semibold">{sprint.sprintName}</h4>
              </div>
              <div className="text-gray-600 mb-4">
                <p className="text-sm">{sprint.sprintDescription}</p>
              </div>
              <div className="text-xs text-gray-500">
                <p className="font-semibold mb-1">Learning Objectives:</p>
                <ul className="list-disc list-inside">
                  {sprint.learningObjectives.map((objective, index) => (
                    <li key={index}>{objective}</li>
                  ))}
                </ul>
              </div>
              <div className="flex items-center text-indigo-600 mt-4">
                <ChevronRight className="w-4 h-4" />
                <span>Start Practice</span>
              </div>
            </button>
          ))}
        </div>
      )}
    </div>
  );
};

export default ProgramWisePractice;
