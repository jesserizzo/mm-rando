#ifndef GIANT_MASK_H
#define GIANT_MASK_H

#include <stdbool.h>
#include <z64.h>

void GiantMask_Handle(ActorPlayer* player, GlobalContext* globalCtx);
f32 GiantMask_GetScaleModifier();
f32 GiantMask_GetSimpleScaleModifier();
f32 GiantMask_GetNextScaleFactor();
bool GiantMask_IsGiant();
void GiantMask_Reset();

#endif // GIANT_MASK_H
