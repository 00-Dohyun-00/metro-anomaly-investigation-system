package com.metro.backend.entity;

import jakarta.persistence.Entity;
import jakarta.persistence.Table;
import jakarta.persistence.Id;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;

@Entity
@Table(name = "operation_cycle")
public class OperationCycle {
  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  private Long id;
}