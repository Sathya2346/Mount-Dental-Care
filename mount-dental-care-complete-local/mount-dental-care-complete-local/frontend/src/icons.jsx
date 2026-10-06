import React from "react";
import {
  Activity, Award, Baby, Bell, CalendarDays, Check, ChevronDown, ChevronRight, ChevronLeft, ChevronUp, ArrowUp, ArrowRight, ArrowLeft,
  CircleHelp, ClipboardCheck, Clock3, Cpu, Eye, Feather, HeartHandshake,
  Mail, MapPin, Menu, Phone, Shield, Smile, Sparkles, Stethoscope, Sun,
  UserRound, UsersRound, Wifi, X, Zap, MessageCircle, Image as ImageIcon,
  Play, ThumbsUp, Target, Layers
} from "lucide-react";

const map = {
  activity: Activity,
  award: Award,
  baby: Baby,
  bell: Bell,
  calendar: CalendarDays,
  clipboard: ClipboardCheck,
  check: Check,
  help: CircleHelp,
  clock: Clock3,
  cpu: Cpu,
  eye: Eye,
  target: Target,
  mission: Target,
  feather: Feather,
  heart: HeartHandshake,
  mail: Mail,
  map: MapPin,
  menu: Menu,
  phone: Phone,
  shield: Shield,
  smile: Smile,
  sparkle: Sparkles,
  sparkles: Sparkles,
  stethoscope: Stethoscope,
  sun: Sun,
  user: UserRound,
  users: UsersRound,
  wifi: Wifi,
  x: X,
  zap: Zap,
  message: MessageCircle,
  image: ImageIcon,
  layers: Layers,
  play: Play,
  thumb: ThumbsUp,
  chevron: ChevronRight,
  chevronLeft: ChevronLeft,
  chevronRight: ChevronRight,
  chevronUp: ChevronUp,
  arrowUp: ArrowUp,
  arrowLeft: ArrowLeft,
  arrowRight: ArrowRight
};

export function Icon({ name, size = 20, strokeWidth = 1.8, ...props }) {
  const C = map[name] || Sparkles;
  return <C size={size} strokeWidth={strokeWidth} {...props} />;
}

export { ChevronDown, ChevronRight, ChevronLeft, ArrowUp };
