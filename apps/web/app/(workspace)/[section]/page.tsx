import { GenericModuleWorkspace } from "@/components/workspace/generic-module-workspace";

export default async function ModulePage({ params }: { params: Promise<{ section: string }> }) {
  const { section } = await params;
  return <GenericModuleWorkspace section={section} />;
}
