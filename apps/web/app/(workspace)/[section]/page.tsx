import { CrmWorkspace } from "@/components/crm/crm-workspace";
import { GenericModuleWorkspace } from "@/components/workspace/generic-module-workspace";

export default async function ModulePage({ params }: { params: Promise<{ section: string }> }) {
  const { section } = await params;
  if (section === "crm") return <CrmWorkspace />;
  return <GenericModuleWorkspace section={section} />;
}
