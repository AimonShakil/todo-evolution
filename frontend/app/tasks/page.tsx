"use client";

/**
 * Tasks Page - Phase II Web App
 *
 * Main task management interface with CRUD operations.
 * Constitutional Principle II: User Data Isolation enforced via JWT.
 */

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";
import { taskApi, type Task } from "@/lib/api-client";

export default function TasksPage() {
  const router = useRouter();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [newTaskTitle, setNewTaskTitle] = useState("");
  const [newTaskDescription, setNewTaskDescription] = useState("");
  const [creating, setCreating] = useState(false);
  const [deleting, setDeleting] = useState<number | null>(null);
  const [editing, setEditing] = useState<number | null>(null);
  const [editTitle, setEditTitle] = useState("");
  const [editDescription, setEditDescription] = useState("");
  const [filter, setFilter] = useState<"all" | "active" | "completed">("all");

  // Get user info from localStorage
  const [userId, setUserId] = useState<number | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [userName, setUserName] = useState<string>("");

  useEffect(() => {
    const storedToken = localStorage.getItem("token");
    const storedUserId = localStorage.getItem("user_id");
    const storedUserName = localStorage.getItem("user_name");

    if (!storedToken || !storedUserId) {
      router.push("/signin");
      return;
    }

    setToken(storedToken);
    setUserId(parseInt(storedUserId));
    setUserName(storedUserName || "User");
  }, [router]);

  useEffect(() => {
    if (userId && token) {
      loadTasks();
    }
  }, [userId, token]);

  const loadTasks = async () => {
    if (!userId || !token) return;

    try {
      setLoading(true);
      const data = await taskApi.getAll(userId, token);
      setTasks(data);
      setError("");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load tasks");
      if (err instanceof Error && err.message.includes("401")) {
        // Token expired or invalid
        localStorage.clear();
        router.push("/signin");
      }
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTask = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!userId || !token || !newTaskTitle.trim()) return;

    try {
      setCreating(true);
      const newTask = await taskApi.create(
        userId,
        {
          title: newTaskTitle,
          description: newTaskDescription || undefined,
        },
        token
      );
      setTasks([newTask, ...tasks]);
      setNewTaskTitle("");
      setNewTaskDescription("");
      setError("");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create task");
    } finally {
      setCreating(false);
    }
  };

  const handleToggleTask = async (task: Task) => {
    if (!userId || !token) return;

    try {
      const updated = await taskApi.toggle(userId, task.id, token);
      setTasks(tasks.map((t) => (t.id === task.id ? updated : t)));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to toggle task");
    }
  };

  const handleDeleteTask = async (taskId: number) => {
    if (!userId || !token || deleting === taskId) return;

    // Prevent double-clicks
    setDeleting(taskId);

    // Optimistic update: Remove from UI immediately
    const previousTasks = tasks;
    setTasks(tasks.filter((t) => t.id !== taskId));
    setError("");

    try {
      await taskApi.delete(userId, taskId, token);
      // Success - task deleted on server
    } catch (err) {
      // Check if it's a 404 (task already deleted) - treat as success
      const errorMessage = err instanceof Error ? err.message : "";
      if (errorMessage.includes("404")) {
        // Task doesn't exist on server (already deleted) - keep UI updated
        console.log("Task already deleted");
      } else {
        // Real error - revert UI and show error
        setTasks(previousTasks);
        setError(errorMessage || "Failed to delete task");
      }
    } finally {
      setDeleting(null);
    }
  };

  const handleStartEdit = (task: Task) => {
    setEditing(task.id);
    setEditTitle(task.title);
    setEditDescription(task.description || "");
    setError("");
  };

  const handleCancelEdit = () => {
    setEditing(null);
    setEditTitle("");
    setEditDescription("");
  };

  const handleSaveEdit = async (taskId: number) => {
    if (!userId || !token || !editTitle.trim()) return;

    try {
      const updated = await taskApi.update(
        userId,
        taskId,
        {
          title: editTitle,
          description: editDescription || undefined,
        },
        token
      );
      setTasks(tasks.map((t) => (t.id === taskId ? updated : t)));
      setEditing(null);
      setEditTitle("");
      setEditDescription("");
      setError("");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to update task");
    }
  };

  const handleSignOut = () => {
    localStorage.clear();
    router.push("/signin");
  };

  // Filter tasks based on selected filter
  const filteredTasks = tasks.filter((task) => {
    if (filter === "active") return !task.completed;
    if (filter === "completed") return task.completed;
    return true; // "all"
  });

  // Task statistics
  const completedCount = tasks.filter((t) => t.completed).length;
  const totalCount = tasks.length;

  if (loading && !userId) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <p className="text-muted-foreground">Loading...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50 p-4">
      <div className="mx-auto max-w-4xl space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold">My Tasks</h1>
            <p className="text-muted-foreground">Welcome back, {userName}!</p>
          </div>
          <Button variant="outline" onClick={handleSignOut}>
            Sign Out
          </Button>
        </div>

        {/* Error Message */}
        {error && (
          <div className="rounded-md bg-destructive/15 p-3 text-sm text-destructive">
            {error}
          </div>
        )}

        {/* Create Task Form */}
        <Card>
          <CardHeader>
            <CardTitle>Create New Task</CardTitle>
            <CardDescription>Add a new task to your list</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleCreateTask} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="title">Title</Label>
                <Input
                  id="title"
                  placeholder="Task title"
                  value={newTaskTitle}
                  onChange={(e) => setNewTaskTitle(e.target.value)}
                  required
                  disabled={creating}
                  maxLength={200}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="description">Description (optional)</Label>
                <Input
                  id="description"
                  placeholder="Task description"
                  value={newTaskDescription}
                  onChange={(e) => setNewTaskDescription(e.target.value)}
                  disabled={creating}
                />
              </div>
              <Button type="submit" disabled={creating || !newTaskTitle.trim()}>
                {creating ? "Creating..." : "Create Task"}
              </Button>
            </form>
          </CardContent>
        </Card>

        {/* Filter Tabs */}
        <Card>
          <CardContent className="pt-6">
            <div className="flex gap-2">
              <Button
                variant={filter === "all" ? "default" : "outline"}
                onClick={() => setFilter("all")}
                className="flex-1"
              >
                All ({totalCount})
              </Button>
              <Button
                variant={filter === "active" ? "default" : "outline"}
                onClick={() => setFilter("active")}
                className="flex-1"
              >
                Active ({totalCount - completedCount})
              </Button>
              <Button
                variant={filter === "completed" ? "default" : "outline"}
                onClick={() => setFilter("completed")}
                className="flex-1"
              >
                Completed ({completedCount})
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Tasks List */}
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-semibold">
              {filteredTasks.length === 0
                ? filter === "all"
                  ? "No tasks yet"
                  : `No ${filter} tasks`
                : `${filteredTasks.length} task${filteredTasks.length === 1 ? "" : "s"}`}
            </h2>
            {totalCount > 0 && (
              <p className="text-sm text-muted-foreground">
                {completedCount} of {totalCount} completed
              </p>
            )}
          </div>

          {loading ? (
            <p className="text-center text-muted-foreground">Loading tasks...</p>
          ) : filteredTasks.length === 0 ? (
            <Card>
              <CardContent className="py-12 text-center text-muted-foreground">
                {filter === "all" ? (
                  <>
                    <p className="text-lg font-medium mb-2">No tasks yet!</p>
                    <p className="text-sm">Create your first task above to get started.</p>
                  </>
                ) : (
                  <p>No {filter} tasks found.</p>
                )}
              </CardContent>
            </Card>
          ) : (
            <div className="space-y-2">
              {filteredTasks.map((task) => (
                <Card key={task.id}>
                  <CardContent className="flex items-start gap-4 pt-6">
                    {editing === task.id ? (
                      // Edit Mode
                      <>
                        <div className="flex-1 space-y-3">
                          <div>
                            <Label htmlFor={`edit-title-${task.id}`}>Title</Label>
                            <Input
                              id={`edit-title-${task.id}`}
                              value={editTitle}
                              onChange={(e) => setEditTitle(e.target.value)}
                              placeholder="Task title"
                              maxLength={200}
                            />
                          </div>
                          <div>
                            <Label htmlFor={`edit-desc-${task.id}`}>Description</Label>
                            <Input
                              id={`edit-desc-${task.id}`}
                              value={editDescription}
                              onChange={(e) => setEditDescription(e.target.value)}
                              placeholder="Task description (optional)"
                            />
                          </div>
                          <div className="flex gap-2">
                            <Button
                              size="sm"
                              onClick={() => handleSaveEdit(task.id)}
                              disabled={!editTitle.trim()}
                            >
                              Save
                            </Button>
                            <Button
                              size="sm"
                              variant="outline"
                              onClick={handleCancelEdit}
                            >
                              Cancel
                            </Button>
                          </div>
                        </div>
                      </>
                    ) : (
                      // View Mode
                      <>
                        <Checkbox
                          checked={task.completed}
                          onCheckedChange={() => handleToggleTask(task)}
                          className="mt-1"
                        />
                        <div className="flex-1">
                          <h3
                            className={`font-medium ${
                              task.completed ? "text-muted-foreground line-through" : ""
                            }`}
                          >
                            {task.title}
                          </h3>
                          {task.description && (
                            <p className="text-sm text-muted-foreground">{task.description}</p>
                          )}
                          <p className="text-xs text-muted-foreground mt-2">
                            Created: {new Date(task.created_at).toLocaleDateString()}
                          </p>
                        </div>
                        <div className="flex gap-2">
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => handleStartEdit(task)}
                          >
                            Edit
                          </Button>
                          <Button
                            variant="destructive"
                            size="sm"
                            onClick={() => handleDeleteTask(task.id)}
                            disabled={deleting === task.id}
                          >
                            {deleting === task.id ? "Deleting..." : "Delete"}
                          </Button>
                        </div>
                      </>
                    )}
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
