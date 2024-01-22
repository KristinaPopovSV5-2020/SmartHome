import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MaterialModule } from 'src/infrastructure/material.module';
import { LinkComponent } from './link/link.component';




@NgModule({
  declarations: [
    LinkComponent,
  ],
  imports: [
    CommonModule,
    MaterialModule
  ],
  exports:[LinkComponent,
  ]
})
export class SharedModule { }
