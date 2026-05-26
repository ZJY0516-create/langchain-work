import { Home, Upload, BookOpen, MessageSquare, Users, Menu, X } from 'lucide-react';
import { useState } from 'react';
import { useLocation, Link } from 'react-router-dom';

interface NavLinkProps {
  to: string;
  children: React.ReactNode;
  icon: React.ReactNode;
}

function NavLink({ to, children, icon }: NavLinkProps) {
  const location = useLocation();
  const isActive = location.pathname === to;
  
  return (
    <Link
      to={to}
      className={`nav-link ${isActive ? 'active' : ''}`}
    >
      {icon} {children}
    </Link>
  );
}

export default function Navigation() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  
  return (
    <nav className="nav-container">
      <div className="nav-content">
        <Link to="/" className="nav-logo">
          <span style={{ fontSize: '1.75rem' }}>🏛️</span>
          <span>文旅智慧助手</span>
        </Link>
        
        <div className="nav-links" style={{ display: mobileMenuOpen ? 'flex' : 'flex' }}>
          <NavLink to="/" icon={<Home size={18} />}>首页</NavLink>
          <NavLink to="/upload" icon={<Upload size={18} />}>智能摘要</NavLink>
          <NavLink to="/knowledge" icon={<BookOpen size={18} />}>知识库</NavLink>
          <NavLink to="/chat" icon={<MessageSquare size={18} />}>智能问答</NavLink>
          <NavLink to="/roleplay" icon={<Users size={18} />}>角色扮演</NavLink>
        </div>
        
        <button
          className="btn-secondary"
          style={{ display: 'none', padding: '0.5rem' }}
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
        >
          {mobileMenuOpen ? <X size={20} /> : <Menu size={20} />}
        </button>
      </div>
    </nav>
  );
}